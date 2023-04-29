package com.example.MozartRealTime;

import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;

import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

public class Permission {
    public static final int REQUEST_CODE = 5;
    // define permissions
    private static final String[] permission = new String[]{
            Manifest.permission.CAMERA,
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
    };
    // check permissions
    public static boolean isPermissionGranted(Activity activity){
        for (String s : permission) {
            int checkPermission = ContextCompat.checkSelfPermission(activity, s);
            if (checkPermission != PackageManager.PERMISSION_GRANTED) {
                return false;
            }
        }
        return true;
    }

    public static boolean checkPermission(Activity activity){
        if(isPermissionGranted(activity)) {
            return true;
        } else {
            ActivityCompat.requestPermissions(activity,permission,REQUEST_CODE);
            return false;
        }
    }
}
