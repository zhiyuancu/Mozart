#include "Common.h"
#include "Logger.h"
using namespace PointCloud;
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include "CameraSystem.h"
#if defined(LINUX) 
#include <sys/wait.h>
#endif
#include <iostream>
#include <fstream>
#include <complex>
#include <bitset>
#include <math.h>
#include <iomanip>
#include <ctime>
#include <sys/time.h>


#include "opencv2/opencv.hpp"

 
using namespace std;
 

void writeMatToFile1(cv::Mat &m, const char* filename)
{
    std::ofstream fout(filename);
    if(!fout){
        std::cout<<"File Not Opened"<<std::endl;
        return;
    }
    for(int i=0;i<m.rows;i++){
        for(int j=0;j<m.cols;j++){
            fout<<m.at<short>(i,j)<<" ";
        }
        fout<<std::endl;
    }
    fout.close();
}

// write data to binary file
void writeMatToFile2(cv::Mat &m, const char* filename)
{
    FILE* pFile;
    int size = 640;
    pFile = fopen(filename,"wb");
    for(int i=0;i<m.rows;i++){
        short row[size];
        for(int j=0;j<m.cols;j++){
            row[j] = m.at<short>(i,j);
        }
        fwrite(row,1,size*sizeof(short),pFile);
    }
    fclose(pFile);
}

Vector<double> _sineTable, _cosineTable;
int phase_count = 4;
int width = 640 ;
int height = 480;
uint32_t phase_length = 460800; // => 640*480*1.5 = 460800
//int modul_fre = 20; //MHz
//float phase_factor = 255*150/(modul_fre*M_PI);
float phase_factor = 255/(M_PI);

int main(int argc,char *argv[]) {
    
    std::cout << "Hello, World!\n";

    // The file to write timestamp
    char timestamp[50] = "./exp/timestamp.txt";
    std::ofstream timefout(timestamp);
    if(!timefout){
        std::cout<<"Timestamp Not Opened"<<std::endl;
        return 0;
    }

    _sineTable.resize(phase_count);
    _cosineTable.resize(phase_count);
	//logger.setDefaultLogLevel(LOG_DEBUG);

     for(auto i = 0; i < phase_count; i++)
    {
        _sineTable[i] = sin(2*M_PI/phase_count*i);
        _cosineTable[i] = cos(2*M_PI/phase_count*i);
        std::cout << "table @" << i << " = " << _sineTable[i] << ", " << _cosineTable[i] << std::endl;
    }
    
    CameraSystem sys;
   
    DevicePtr     device;
    const Vector<DevicePtr> &devices = sys.scan();
    bool found = false;
    int frame_count = 0;
    for (auto &d: devices){
		std::cout <<  " ||| Detected devices: "  << d->id() << std::endl;
        device = d;
        found = true;
    }
    if (!found){
		std::cout <<  " ||| No device found "  << std::endl;
      return 0;
    }
    DepthCameraPtr depthCamera;
    depthCamera = sys.connect(device);
    if (!depthCamera) {
		std::cout << " ||| Could not load depth camera for device "<< device->id() << std::endl;
        return 1;
    }

    FrameRate r;
    if(depthCamera->getFrameRate(r))
		std::cout << " ||| Capturing at a frame rate of " << r.getFrameRate() << " fps" << std::endl;
    r.numerator = 30;
    depthCamera->setFrameRate(r);
    if(depthCamera->getFrameRate(r))
		std::cout << " ||| Capturing at a frame rate of " << r.getFrameRate() << " fps" << std::endl;
    
    unsigned int intg_time;
    intg_time = 105;
    depthCamera->set("intg_time",intg_time);
    depthCamera->get("intg_time",intg_time);
    std::cout<<" ||| INTG_TIME :  " << intg_time  << std::endl;
//    logger(LOG_INFO) << " ||| INTG_TIME :  " << intg_time  << std::endl;
    
    
    FrameSize s;
    if(depthCamera->getFrameSize(s))
		std::cout << " ||| Frame size :  " << s.width << " * "<< s.height << std::endl;
    int centerPointIndex = (s.height/2 ) * s.width + s.width/2;
    
    if (!depthCamera->isInitialized()) {
		std::cout << " ||| Depth camera not initialized for device "<< device->id() << std::endl;
        return 1;
    }
    std::cout << " ||| Successfully loaded depth camera for device " << std::endl;
    
    
    
    // Must register one callback before starting capture 
    //depthCamera->registerCallback(DepthCamera::FRAME_RAW_FRAME_UNPROCESSED,rawABdataCallback);
    
     depthCamera->registerCallback(DepthCamera::FRAME_RAW_FRAME_UNPROCESSED, [&](DepthCamera &dc, const Frame &frame, DepthCamera::FrameType frameType) {
         const RawDataFrame *rawDataFrame = dynamic_cast<const RawDataFrame *>(&frame);
         if(!rawDataFrame)
         {
           std::cout << "Null frame captured? or not of type RawDataFrame" << std::endl;
           return;
         }
         
         std::cout << " frame : " <<  rawDataFrame->id  << " size: " << rawDataFrame->data.size() << std::endl;
         if ( rawDataFrame->data.size() != 1843596 ){
            std::cout << " Data size not correct ! Register FRAME_RAW_FRAME_UNPROCESSED only on registerCallback function to get the correct raw A-B data."<< std::endl;
         }

         // print the timestamp of this frame
        struct timeval tv;
        gettimeofday(&tv, NULL);
        timefout << frame_count << " " << long(tv.tv_sec * 1e6 + tv.tv_usec) << endl;
        
        // << " " << tv.tv_sec << " " << tv.tv_usec 
         
         // For id usage:
         // If you using two modulation frequency ，
         // below id field will show the modulation frequency number for reference
         // For data size ：
         // default value should be 1843596 for 640*480 and 4 phases , every pixel using 1.5 byte
         // 640*480 * 1.5 * 4 = 1843200 , another 396 byte additional information at the end
         uint8_t *in = (uint8_t *)rawDataFrame->data.data();
        
         auto index = 0,idx2=0;
         uint16_t amp, pha;
         float phase;
         int k = 0;
         int virtual_interference = 0;
        
         Complex c_res;
         Complex c_diff;
         int gap = 30;
         float factor = 255.0/1024;

         cv::Mat tof_1=cv::Mat::zeros(height,width,CV_16SC1);
         short *pamp_1 = (short*)(tof_1.data);

         cv::Mat tof_2=cv::Mat::zeros(height,width,CV_16SC1);
         short *pamp_2 = (short*)tof_2.data;

         cv::Mat tof_3=cv::Mat::zeros(height,width,CV_16SC1);
         short *pamp_3 = (short*)tof_3.data;

         cv::Mat tof_4=cv::Mat::zeros(height,width,CV_16SC1);
         short *pamp_4 = (short*)tof_4.data;
         
         char filename_1[50] = { 0 };
         char filename_2[50] = { 0 };
         char filename_3[50] = { 0 };
         char filename_4[50] = { 0 };
         
         sprintf(filename_1, "./exp/frame_%d_1.txt", frame_count);
         sprintf(filename_2, "./exp/frame_%d_2.txt", frame_count);
         sprintf(filename_3, "./exp/frame_%d_3.txt", frame_count);
         sprintf(filename_4, "./exp/frame_%d_4.txt", frame_count);

         
         for(int j = 0;j< width*height;j+=2)
         {
             // calculate two pixel at the same time
             double ii = 0, iq = 0;
             double ii1 = 0, iq1 = 0;
             
             int16_t r1,r2,r3,r4;
             for(int i=0;i<phase_count;i++)
             {
                 
                 int16_t a_b = in[i*phase_length + index];
                 int16_t a_b1 = in[i*phase_length + index+1];

                 a_b = (a_b << 4) | (0xf & in[i*phase_length + index+2]);
                 a_b1 = (a_b1 << 4) | ((0xf0 & in[i*phase_length + index+2])>>4);

                 a_b = (((int16_t)(a_b << 4) )>>4);
                 a_b1 = (((int16_t)(a_b1 << 4))>>4);
                 
                 ii += a_b*_cosineTable[i];
                 iq += a_b*_sineTable[i];
                 ii1 += a_b1*_cosineTable[i];
                 iq1 += a_b1*_sineTable[i];
                  
                 //frame 0
                 if(i==0){
                     *(pamp_1 + k) = int(a_b);
                     k+=1;
                     *(pamp_1 + k) = int(a_b1);
                     k+=1;
                 }
                 
                 //frame 1
                 if(i==1){
                     *(pamp_2 + k) = int(a_b);
                     k+=1;
                     *(pamp_2 + k) = int(a_b1);
                     k+=1;
                 }
                 
//                 frame 2
                 if(i==2){
                     *(pamp_3 + k) = int(a_b);
                     k+=1;
                     *(pamp_3 + k) = int(a_b1);
                     k+=1;
                 }

                 //frame 3
                 if(i==3){
                     *(pamp_4 + k) = int(a_b);
                     k+=1;
                     *(pamp_4 + k) = int(a_b1);
                     k+=1;
                 }
                 k-=2;
             }
             
//             *(pamp_5+k) = int(round(ii));
//             *(pamp_6+k) = int(round(iq));
             k+=1;
//             *(pamp_5+k) = int(round(ii1));
//             *(pamp_6+k) = int(round(iq1));
             k+=1;
             idx2 +=4;
             index += 3;
         }
         frame_count++;
         cout<<"frame count: "<<frame_count<<endl;

         writeMatToFile2(tof_1,filename_1);
         writeMatToFile2(tof_2,filename_2);
         writeMatToFile2(tof_3,filename_3);
         writeMatToFile2(tof_4,filename_4);
     });

    if(depthCamera->start()){
          logger(LOG_INFO) <<  " ||| start camera pass" << std::endl;
          
    }else{
        logger(LOG_INFO) <<  " ||| start camera fail" << std::endl;  
    }
       
    std::cout << "Press any key to quit" << std::endl;
    getchar();
    depthCamera->stop();
    sys.disconnect(depthCamera,true);
    
}

