#version 300 es
precision highp float;in vec2 vUv;out vec4 fragColor;uniform float uVpd;uniform float uTime;
void main(){vec2 p=vUv-.5;float field=exp(-length(p-vec2(sin(uTime*.2)*.12,cos(uTime*.15)*.1))*(4.+uVpd));vec3 dry=vec3(.75,.25,.12),humid=vec3(.03,.48,.34);fragColor=vec4(mix(humid,dry,clamp(uVpd/2.,0.,1.))*(.25+.75*field),1.);}
