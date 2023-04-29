package com.example.MozartRealTime;

import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.ImageFormat;
import android.media.Image;
import android.media.ImageReader;
import android.os.Environment;
import android.util.Log;

import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ShortBuffer;
import java.nio.channels.FileChannel;
import java.text.SimpleDateFormat;
import java.util.Date;

public class DepthFrameAvailableListener implements ImageReader.OnImageAvailableListener {
    private static final String TAG = DepthFrameAvailableListener.class.getSimpleName();

    public static int WIDTH = 640;
    public static int HEIGHT = 480;

    private static float RANGE_MIN = 100.0f;
    private static float RANGE_MAX = 1000.f;
    private static float CONFIDENCE_FILTER = 0.1f;

    private DepthFrameVisualizer depthFrameVisualizer;
    private int[] rawMask;
    public String startTime;

    private String currentTime;
    private final SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd-hh.mm.ss.SSS");
    private File csvFileName;

    public DepthFrameAvailableListener(DepthFrameVisualizer depthFrameVisualizer, String start) {
        this.depthFrameVisualizer = depthFrameVisualizer;

        int size = WIDTH * HEIGHT;
        rawMask = new int[size];
        startTime = start;

        // write the header of CSV
        String root = Environment.getExternalStorageDirectory().getAbsolutePath();
        File dir = new File(root + String.format("/depth_record/%s", startTime));
        dir.mkdirs();
        csvFileName = new File(dir, "log.csv");

        String header = "timeStamp,interval(ms)\n";
        writeCsvRow(header);

    }

    @Override
    public void onImageAvailable(ImageReader reader) {
        try {
            //start time: before acquiring data
            Date start = new Date();
            Image image = reader.acquireNextImage();

            //dataCollection: after acquiring data
            Date dataCollection = new Date();

            if (image != null && image.getFormat() == ImageFormat.DEPTH16) {
                currentTime = simpleDateFormat.format(new Date());
                //saveToInternalStorage(bytes, startTime, currentTime);
                int depthWidth = image.getWidth();
                int depthHeight = image.getHeight();
                Log.d("Image width: ", String.format("%d", depthWidth));
                Log.d("Image height: ", String.format("%d", depthHeight));

                // process image

                processImage(image);

                // end time: after processing the Mozart map
                Date end = new Date();

                // write fps to csv file
                long timeCollect = (dataCollection.getTime() - start.getTime())*10;
                long timeProcess = end.getTime() - dataCollection.getTime();
                String row = String.format("%s, %d, %d\n", currentTime, timeCollect, timeProcess);
                Log.d("Time for each frame: ", row);
                writeCsvRow(row);

                // render depth image to surface
                publishRawData();

                // write image to storage
                writeDepth16(image, startTime, currentTime);
            }
            assert image != null;
            image.close();
        }
        catch (Exception e) {
            Log.e(TAG, "Failed to acquireNextImage: " + e.getMessage());
        }
    }

    private void writeCsvRow(String row){
        try {
            FileWriter csvWriter = new FileWriter(csvFileName, true);
            csvWriter.write(row);
            csvWriter.flush();
            csvWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void writeDepth16(Image depthImage, String startTime, String currentTime){
        if(depthImage.getFormat() != ImageFormat.DEPTH16)
            throw new RuntimeException("Expected image format is DEPTH16, but is:"+depthImage.getFormat());

        ByteBuffer buffer = depthImage.getPlanes()[0].getBuffer();

        String root = Environment.getExternalStorageDirectory().getAbsolutePath();
        File myDir = new File(root + String.format("/depth_record/%s", startTime));
        myDir.mkdirs();
        File myPath = new File (myDir, String.format("raw_%s.txt", currentTime));

        try {
            FileChannel fc = new FileOutputStream(myPath).getChannel();
            // Use the compress method on the BitMap object to write image to the OutputStream
            fc.write(buffer);
            Log.d("file saved to", String.format("raw_%s.txt", currentTime));
            fc.close();
        } catch (IOException e) {
            e.printStackTrace();
            Log.i(TAG, "Error writing image depth16: " +myPath.getPath());
        }
    }

    private void publishRawData() {
        if (depthFrameVisualizer != null) {
            Bitmap bitmap = convertToRGBBitmap(rawMask);
            depthFrameVisualizer.onRawDataAvailable(bitmap);
            bitmap.recycle();
        }
    }

    private void processImage(Image image) {
        ShortBuffer shortDepthBuffer = image.getPlanes()[0].getBuffer().asShortBuffer();
        for (int y = 0; y < HEIGHT; y++) {
            for (int x = 0; x < WIDTH; x++) {
                int index = y * WIDTH + x;
                short depthSample = shortDepthBuffer.get(index);
//                int newValue = calculateMozart(depthSample, CONFIDENCE_FILTER);
                int depthRange = (short) (depthSample & 0x1FFF);
                int depthConfidence = (short) ((depthSample >> 13) & 0x7);
                int depthratio = depthConfidence == 0 ? 7 : (depthConfidence-1);
                float depthPercentage = depthConfidence == 0 ? 1.f : (depthConfidence - 1) * 0.142857143f;

                float cutDepth = (float) (normalizeRange(depthRange) * 0.0039215686);
                float N2 = depthPercentage * cutDepth;
                float N1 = depthPercentage * (1 - cutDepth);
                float MozartFloat = (float) Math.sqrt(N2 * N2 * (depthratio));
                int newValue = (int)(MozartFloat * 255);
                // Store value in the rawMask for visualization
                rawMask[index] = newValue;
//                rawMask[index] = depthConfidence * 255 / 7;
            }
        }
    }

    private int calculateMozart(short sample, float confidenceFilter) {
        int depthRange = (short) (sample & 0x1FFF);
        int depthConfidence = (short) ((sample >> 13) & 0x7);
        float depthPercentage = depthConfidence == 0 ? 1.f : (depthConfidence - 1) / 7.f;
        int depthratio = depthConfidence == 0 ? 7 : (depthConfidence - 1);
        float cutDepth = (float) (normalizeRange(depthRange) / 255.);
        float N2 = depthPercentage * cutDepth;
//        float N1 = depthPercentage * (1 - cutDepth);
        float MozartFloat = (float) Math.atan(N2 * N2 * (depthratio));
//        float MozartFloat = 0.5F;
//        float MozartFloat = (float)(N2 * N2 / (N1 + N2 + 1e-6));
        return (int) Math.round(MozartFloat * 255.);
    }

    private Bitmap convertToRGBBitmap(int[] mask) {
        Bitmap bitmap = Bitmap.createBitmap(WIDTH, HEIGHT, Bitmap.Config.ARGB_4444);
        for (int y = 0; y < HEIGHT; y++) {
            for (int x = 0; x < WIDTH; x++) {
                int index = y * WIDTH + x;
                bitmap.setPixel(x, y, Color.argb(255, mask[index], mask[index],mask[index]));
            }
        }
        return bitmap;
    }

    private int normalizeRange(int range) {
        float normalized = (float)range - RANGE_MIN;
        // Clamp to min/max
        normalized = Math.max(RANGE_MIN, normalized);
        normalized = Math.min(RANGE_MAX, normalized);
        // Normalize to 0 to 255
        normalized = normalized - RANGE_MIN;
        normalized = normalized / (RANGE_MAX - RANGE_MIN) * 255;
        return (int)normalized;
    }

}