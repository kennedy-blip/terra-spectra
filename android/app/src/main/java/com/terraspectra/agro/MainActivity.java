package com.terraspectra.agro;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(android.os.Bundle savedInstanceState) {
        registerPlugin(TerraSensorPlugin.class);
        registerPlugin(BioAcousticAudioPlugin.class);
        super.onCreate(savedInstanceState);
    }
}
