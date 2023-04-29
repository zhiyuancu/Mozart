package com.example.MozartRealTime;

import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Matrix;
import android.graphics.RectF;
import android.os.Bundle;
import android.view.TextureView;

import androidx.appcompat.app.AppCompatActivity;

import java.text.SimpleDateFormat;
import java.util.Date;

/*  This is an example of getting and processing ToF data.

    This example will only work (correctly) on a device with a front-facing depth camera
    with output in DEPTH16. The constants can be adjusted but are made assuming this
    is being run on a Samsung S10 5G device.
 */
public class MainActivity extends AppCompatActivity implements DepthFrameVisualizer {
    private static final String TAG = MainActivity.class.getSimpleName();
    public static final int CAM_PERMISSIONS_REQUEST = 0;

    private TextureView rawDataView;
    private Matrix defaultBitmapTransform;
    private Camera camera;

    private String startTime;
    private final SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd-hh.mm.ss");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        rawDataView = findViewById(R.id.rawData);

        Permission.checkPermission(this);
        startTime = simpleDateFormat.format(new Date());

        camera = new Camera(this, this, startTime);
        camera.openFrontDepthCamera();

    }


    @Override
    public void onRawDataAvailable(Bitmap bitmap) {
        renderBitmapToTextureView(bitmap, rawDataView);
    }

    /* We don't want a direct camera preview since we want to get the frames of data directly
        from the camera and process.

        This takes a converted bitmap and renders it onto the surface, with a basic rotation
        applied.
     */
    private void renderBitmapToTextureView(Bitmap bitmap, TextureView textureView) {
        Canvas canvas = textureView.lockCanvas();
        canvas.drawBitmap(bitmap, defaultBitmapTransform(textureView), null);
        textureView.unlockCanvasAndPost(canvas);
    }

    private Matrix defaultBitmapTransform(TextureView view) {
        if (defaultBitmapTransform == null || view.getWidth() == 0 || view.getHeight() == 0) {
            Matrix matrix = new Matrix();
            int centerX = view.getWidth() / 2;
            int centerY = view.getHeight() / 2;

            int bufferWidth = DepthFrameAvailableListener.WIDTH;
            int bufferHeight = DepthFrameAvailableListener.HEIGHT;

            RectF bufferRect = new RectF(0, 0, bufferWidth, bufferHeight);
            RectF viewRect = new RectF(0, 0, view.getWidth(), view.getHeight());
            matrix.setRectToRect(bufferRect, viewRect, Matrix.ScaleToFit.CENTER);
            matrix.postRotate(90, centerX, centerY);

            defaultBitmapTransform = matrix;
        }
        return defaultBitmapTransform;
    }
}






