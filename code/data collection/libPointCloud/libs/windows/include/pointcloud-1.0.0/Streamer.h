/*
 * PointCloud Lib component.
 *
 * Copyright (c) 2018 PointCloud.ai Inc.
 */

#ifndef POINTCLOUD_STREAMER_H
#define POINTCLOUD_STREAMER_H

#include "Device.h"
#include "Frame.h"
#include "VideoMode.h"
#include "Timer.h"

namespace PointCloud
{
/**
 * \addtogroup IO
 * @{
 */


class POINTCLOUD_EXPORT Streamer
{
protected:
  DevicePtr _device;
  
  Timer _time;
  
  int _currentID = -1;
  TimeStampType _currentTimeStamp = 0;
  
  bool _isRunning = false;
  
  virtual bool _start() = 0;
  virtual bool _capture(RawDataFramePtr &p) = 0;
  virtual bool _stop() = 0;
  
public:
  Streamer(DevicePtr device): _device(device) {}
  
  virtual ~Streamer();
  
  virtual bool isInitialized() = 0;
  virtual bool isRunning() { return _isRunning; }
  
  virtual bool start();
  virtual bool capture(RawDataFramePtr &p);
  virtual bool stop();
  
  virtual bool getSupportedVideoModes(Vector<VideoMode> &videoModes) = 0;
  
  virtual bool getCurrentVideoMode(VideoMode &videoMode) = 0;
  virtual bool setVideoMode(const VideoMode &videoMode) = 0;
};
/**
 * @}
 */

}

#endif // STREAMER_H