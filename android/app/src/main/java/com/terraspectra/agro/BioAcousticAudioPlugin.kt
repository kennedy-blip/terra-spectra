package com.terraspectra.agro

import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder
import com.getcapacitor.*
import com.getcapacitor.annotation.CapacitorPlugin
import java.util.concurrent.atomic.AtomicBoolean

@CapacitorPlugin(name = "BioAcousticAudio")
class BioAcousticAudioPlugin : Plugin() {
    private var recorder: AudioRecord? = null
    private val running = AtomicBoolean(false)
    @PluginMethod fun start(call: PluginCall) {
        val rate = 16000; val size = AudioRecord.getMinBufferSize(rate, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT).coerceAtLeast(4096)
        try { recorder = AudioRecord(MediaRecorder.AudioSource.UNPROCESSED, rate, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT, size) } catch (e: SecurityException) { call.reject("Microphone permission required", e); return }
        if (recorder?.state != AudioRecord.STATE_INITIALIZED) { call.reject("Audio input unavailable"); return }
        running.set(true); recorder?.startRecording(); call.resolve(JSObject().put("sampleRate", rate).put("bufferBytes", size))
        Thread { val buffer = ShortArray(size / 2); while (running.get()) { val n = recorder?.read(buffer, 0, buffer.size) ?: -1; if (n > 0) notifyListeners("pcm", JSObject().put("samples", JSArray(buffer.take(n).map { it.toInt() }))) } }.start()
    }
    @PluginMethod fun stop(call: PluginCall) { running.set(false); recorder?.run { stop(); release() }; recorder = null; call.resolve() }
    override fun handleOnDestroy() { running.set(false); recorder?.release(); recorder = null; super.handleOnDestroy() }
}
