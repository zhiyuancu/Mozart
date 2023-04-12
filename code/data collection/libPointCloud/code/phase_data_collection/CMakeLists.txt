project(get_raw_phase)

find_library(LIBUSB_LIBS  
  NAMES  usb 
  PATHS  /usr/local/lib  
)

find_package( OpenCV REQUIRED )

add_definitions(-std=c++11)
INCLUDE_DIRECTORIES(../../libs/macos/include/pointcloud-1.0.0/)
LINK_DIRECTORIES(/Users/xiezhiyuan/libPointCloud/libs/macos/lib/)

add_executable(get_raw_phase get_raw_phase.cpp)
target_link_libraries(get_raw_phase pointcloud ${OpenCV_LIBS})