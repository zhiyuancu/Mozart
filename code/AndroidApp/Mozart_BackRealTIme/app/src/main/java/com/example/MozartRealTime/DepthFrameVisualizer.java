package com.example.MozartRealTime;

import android.graphics.Bitmap;

public interface DepthFrameVisualizer {
    void onRawDataAvailable(Bitmap bitmap);
}
