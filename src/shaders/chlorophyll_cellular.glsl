#version 300 es
precision highp float;
in vec2 vUv; out vec4 fragColor; uniform float uTime; uniform float uHealth;
float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x),f.y);}
void main(){vec2 uv=vUv;float n=noise(uv*7.+uTime*.08)+.45*noise(uv*15.-uTime*.04);float cell=smoothstep(.35,.8,n);vec3 healthy=vec3(.02,.35,.18);vec3 alert=vec3(.55,.17,.04);vec3 color=mix(alert,healthy,clamp(uHealth,0.,1.));color+=vec3(.02,.14,.08)*cell;fragColor=vec4(color,1.);}
