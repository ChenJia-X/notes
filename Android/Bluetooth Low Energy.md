# [Bluetooth Low Energy](https://developer.android.com/guide/topics/connectivity/bluetooth-le.html#permissions)

## Key Terms and Concepts

- **Generic Attribute Profile (GATT)**
- **Attribute Protocol (ATT)**
- **Characteristic**
- **Descriptor**
- **Service**

### Roles and Responsibilitie

- client
- server

### Android BLE API 简介

[BluetoothAdapter](https://developer.android.com/reference/android/bluetooth/BluetoothAdapter.html)
BluetoothAdapter 拥有基本的蓝牙操作，例如开启蓝牙扫描，使用已知的 MAC 地址 （BluetoothAdapter#getRemoteDevice）实例化一个 BluetoothDevice 用于连接蓝牙设备的操作等等。

BluetoothAdapter.LeScanCallback

This is the interface used to deliver BLE scan results.

[BluetoothDevice](https://developer.android.com/reference/android/bluetooth/BluetoothDevice.html)
代表一个远程蓝牙设备。这个类可以让你连接所代表的蓝牙设备或者获取一些有关它的信息，例如它的名字，地址和绑定状态等等。

[BluetoothGatt](https://developer.android.com/reference/android/bluetooth/BluetoothGatt.html)
这个类提供了 Bluetooth GATT 的基本功能。例如重新连接蓝牙设备，发现蓝牙设备的 Service 等等。

BluetoothGattCallback

This is used to deliver results to the client, such as connection status, as well as any further GATT client operations.

[BluetoothGattService](https://developer.android.com/reference/android/bluetooth/BluetoothGattService.html)
这一个类通过 BluetoothGatt#getService 获得，如果当前服务不可见那么将返回一个 null。这一个类对应上面说过的 Service。我们可以通过这个类的 getCharacteristic(UUID uuid) 进一步获取 Characteristic 实现蓝牙数据的双向传输。

[BluetoothGattCharacteristic](https://developer.android.com/reference/android/bluetooth/BluetoothGattCharacteristic.html)
这个类对应上面提到的 Characteristic。通过这个类定义需要往外围设备写入的数据和读取外围设备发送过来的数据。

## BLE Permissions

1. Basis permissions

   ```xml
   <uses-permission android:name="android.permission.BLUETOOTH"/>
   <uses-permission android:name="android.permission.BLUETOOTH_ADMIN"/>
   ```

2. If you want to declare that your app is **available to BLE-capable devices only**, include the following in your app's manifest:

   ```xml
   <uses-feature android:name="android.hardware.bluetooth_le" android:required="true"/>
   ```

   - However, if you want to make your **app available to devices that don't support BLE**, you should still include this element in your app's manifest, but set `required="false"`. Then at run-time you can determine BLE availability by using `PackageManager.hasSystemFeature()`:

     ```java
     // Use this check to determine whether BLE is supported on the device. Then
     // you can selectively disable BLE-related features.
     if (!getPackageManager().hasSystemFeature(PackageManager.FEATURE_BLUETOOTH_LE)) {
         Toast.makeText(this, R.string.ble_not_supported, Toast.LENGTH_SHORT).show();
         finish();
     }
     ```

3. Requesting User Permissions

   In order to receive location updates from `NETWORK_PROVIDER` or `GPS_PROVIDER`, you must request the user's permission by declaring either the {@code ACCESS_COARSE_LOCATION} or {@code ACCESS_FINE_LOCATION} permission.	

   - If you are using both `NETWORK_PROVIDER` and `GPS_PROVIDER`, then you need to request only the {@code ACCESS_FINE_LOCATION} permission, because it includes permission for both providers. 

   - **Caution:** If your app targets Android 5.0 (API level 21) or higher, you *must* declare that your app uses the `android.hardware.location.network` or`android.hardware.location.gps` hardware feature in the manifest file...

     ```xml
     <manifest ... >
         <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
         ...
         <!-- Needed only if your app targets Android 5.0 (API level 21) or higher. -->
         <uses-feature android:name="android.hardware.location.gps" />
         ...
     </manifest>
     ```

## Setting up BLE

>  Before your application can communicate over BLE, you need to **verify that BLE is supported on the device**, and if so, ensure that it is enabled.
>
>  - Note that this check is **only necessary** if `<uses-feature.../>` is set to false.

If BLE is not supported, then you should gracefully disable any BLE features. 

If BLE is supported, but disabled, then you can request that the user enable Bluetooth without leaving your application. 

1. Get the BluetoothAdapter

   ```java
   private BluetoothAdapter mBluetoothAdapter;
   ...
   // Initializes Bluetooth adapter.
   final BluetoothManager bluetoothManager =
           (BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE);
   mBluetoothAdapter = bluetoothManager.getAdapter();
   ```

2. Enable Bluetooth

   If `isEnabled()` returns false, the snippet displays an error prompting the user to go to Settings to enable Bluetooth.

   ```java
   // Ensures Bluetooth is available on the device and it is enabled. If not,
   // displays a dialog requesting user permission to enable Bluetooth.
   if (mBluetoothAdapter == null || !mBluetoothAdapter.isEnabled()) {
       Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
       startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
   }

   ...
   @Override
   protected void onActivityResult(int requestCode, int resultCode, Intent data) {
     // User chose not to enable Bluetooth.
     if (requestCode == REQUEST_ENABLE_BT && resultCode == Activity.RESULT_CANCELED) {
       finish();
       return;
     }
     super.onActivityResult(requestCode, resultCode, data);
   }

   ```

## Finding BLE Devices

> To find BLE devices, you use the `startLeScan()` method. This method takes a `BluetoothAdapter.LeScanCallback` as a parameter. You must implement this callback, because that is how scan results are returned.

Because scanning is battery-intensive, you should observe the following guidelines:

- As soon as you find the desired device, stop scanning.
- Never scan on a loop, and set a time limit on your scan. A device that was previously available may have moved out of range, and continuing to scan drains the battery.

1. The following snippet shows how to start and stop a scan:

```java
/**
 * Activity for scanning and displaying available BLE devices.
 */
public class DeviceScanActivity extends ListActivity {

    private BluetoothAdapter mBluetoothAdapter;
    private boolean mScanning;
    private Handler mHandler;

    // Stops scanning after 10 seconds.
    private static final long SCAN_PERIOD = 10000;
    ...
    private void scanLeDevice(final boolean enable) {
        if (enable) {
            // Stops scanning after a pre-defined scan period.
            mHandler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    mScanning = false;
                    mBluetoothAdapter.stopLeScan(mLeScanCallback);
                }
            }, SCAN_PERIOD);

            mScanning = true;
            mBluetoothAdapter.startLeScan(mLeScanCallback);
        } else {
            mScanning = false;
            mBluetoothAdapter.stopLeScan(mLeScanCallback);
        }
        ...
    }
...
}
```



- If you want to scan for only specific types of peripherals, you can instead call `startLeScan(UUID[], BluetoothAdapter.LeScanCallback)`, providing an array of `UUID` objects that specify the GATT services your app supports.

2. Here is an implementation of the `BluetoothAdapter.LeScanCallback`, which is the interface used to deliver BLE scan results:

   ```java
   private LeDeviceListAdapter mLeDeviceListAdapter;
   ...
   // Device scan callback.
   private BluetoothAdapter.LeScanCallback mLeScanCallback =
           new BluetoothAdapter.LeScanCallback() {
       @Override
       public void onLeScan(final BluetoothDevice device, int rssi,
               byte[] scanRecord) {
           runOnUiThread(new Runnable() {
              @Override
              public void run() {
                  mLeDeviceListAdapter.addDevice(device);
                  mLeDeviceListAdapter.notifyDataSetChanged();
              }
          });
      }
   };
   ```

> **Note:** You can only scan for Bluetooth LE devices *or* scan for Classic Bluetooth devices, as described in [Bluetooth](https://developer.android.com/guide/topics/connectivity/bluetooth.html). You cannot scan for both Bluetooth LE and classic devices at the same time.

## Connecting to a GATT Server

To connect to a GATT server on a BLE device, you use the `connectGatt()` method. 

This method takes three parameters: 

- a `Context` object, 
- `autoConnect` (boolean indicating whether to automatically connect to the BLE device as soon as it becomes available),
- and a reference to a `BluetoothGattCallback`:

```java
mBluetoothGatt = device.connectGatt(this, false, mGattCallback);
```



## Reading BLE Attributes



## Receiving GATT Notifications



## Closing the Client App