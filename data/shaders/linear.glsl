
uniform vec2 start;
uniform vec2 end;

uniform float canvasHeight;
uniform vec4 stops;

uniform vec4 stop0;
uniform vec4 stop1;
uniform vec4 stop2;
uniform vec4 stop3;
uniform vec4 stop4;

uniform mat3 invGradientTransform;

varying vec4 location; 

void main()
{
    vec4 result;
    
    vec3 transformed = invGradientTransform*vec3(location.x, location.y, 1);
    //return ((pt[0] - self.x1)*(self.x2 - self.x1) + (pt[1] - self.y1)*(self.y2 - self.y1)) / ((self.x1 - self.x2)**2 + (self.y1 - self.y2)**2)
    
    float num = (transformed.x - start.x)*(end.x - start.x) + (transformed.y - start.y)*(end.y - start.y);
    float denom = pow(abs(start.x - end.x), 2.0) + pow(abs(start.y - end.y), 2.0);
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