package com.terraspectra.agro

import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import com.getcapacitor.*
import com.getcapacitor.annotation.CapacitorPlugin

@CapacitorPlugin(name = "TerraSensor")
class TerraSensorPlugin : Plugin(), SensorEventListener {
    private lateinit var manager: SensorManager
    override fun load() { manager = context.getSystemService(Context.SENSOR_SERVICE) as SensorManager }
    @PluginMethod fun startWatch(call: PluginCall) {
        val type = when (call.getString("sensor")) { "light" -> Sensor.TYPE_LIGHT; "pressure" -> Sensor.TYPE_PRESSURE; "rotation" -> Sensor.TYPE_ROTATION_VECTOR; else -> Sensor.TYPE_RELATIVE_HUMIDITY }
        val sensor = manager.getDefaultSensor(type)
        if (sensor == null) { call.reject("Requested sensor is unavailable"); return }
        manager.registerListener(this, sensor, SensorManager.SENSOR_DELAY_UI); call.resolve(JSObject().put("active", true).put("sensor", sensor.name))
    }
    override fun onSensorChanged(event: SensorEvent) { notifyListeners("telemetry", JSObject().put("type", event.sensor.type).put("value", event.values[0].toDouble())) }
    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}
    override fun handleOnStop() { if (::manager.isInitialized) manager.unregisterListener(this); super.handleOnStop() }
}
