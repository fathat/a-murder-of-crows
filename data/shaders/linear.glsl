
uniform vec2 start;
uniform vec2 end;

uniform float canvasHeight;
uniform vec4 stops;

uniform vec4 stop0;
uniform vec4 stop1;
uniform vec4 stop2;
uniform vec4 stop3;
uniform vec4 stop4;

uniform mat3 worldTransform;
uniform mat3 gradientTransform;
uniform mat3 invGradientTransform;

varying vec4 worldCoords;
varying vec4 localCoords; 

void main()
{
    vec4 result;
            
    vec3 s = gradientTransform*vec3(start.x, start.y, 1);
    vec3 d = gradientTransform*vec3(end.x, end.y, 1); 
    vec3 l = localCoords.xyz;
        
    float num = (l.x - s.x)*(d.x - s.x) + (l.y - s.y)*(d.y - s.y);
    float denom = pow(abs(s.x - d.x), 2.0) + pow(abs(s.y - d.y), 2.0);
    float intensity =  clamp(num / denom, 0.0, 1.0);

    //calculate the intensity
    if(intensity <= stops.x)
    {
        result.rgba = mix(stop0, stop1, (intensity / stops.x));
    }
    else if(intensity <= stops.y)
    {
        result.rgba = mix(stop1, stop2, (intensity-stops.x) / (stops.y-stops.x));
    }
    else if(intensity <= stops.z)
    {
        result.rgba = mix(stop2, stop3, (intensity-stops.y) / (stops.z-stops.y));
    }
    else if(intensity <= stops.w)
    {
        result.rgba = mix(stop3, stop4, (intensity-stops.z) / (stops.w-stops.z));
    }
    
    gl_FragColor = result;
}