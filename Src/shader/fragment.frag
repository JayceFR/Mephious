#version 330 

uniform sampler2D tex;
uniform sampler2D ui_tex;
uniform float time;

uniform sampler2D noise_tex1;
uniform int itime;
uniform int corrupted;

uniform float time_scale = 0.25;
uniform float angle_Const = 0.5;
uniform float stripeWidth = 20;
uniform float stripeImpact = 0.03;
uniform float threshold = 0.3;

in vec2 uvs;
out vec4 f_color;

vec2 random2( vec2 p ) {
    return fract(sin(vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3))))*43758.5453);
}

void overlay_frag(){
    //f_color = vec4(texture(tex, uvs).rgb ,1.0);
    vec2 px_uvs = vec2(floor(uvs.x * 320) / 320, floor(uvs.y * 210) / 210);
    float center_dis = distance(uvs, vec2(0.5,0.5));
    float noise_val = center_dis + texture(noise_tex1, vec2(px_uvs.x * 1.52 * 2 + itime * 0.001, px_uvs.y * 2)).r * 0.2;
    vec4 dark = vec4(0.086, 0.4549, 0.196, 1.0);
    dark = vec4(0.0, 0.0, 0.0, 1.0);
    float darkness = max(0, noise_val - 0.7) * 20;
    //float vignette = max(0, center_dis * center_dis - 0.5) * 20;
    darkness += center_dis;
    f_color = darkness * dark + (1 - darkness) * f_color;
    vec4 ui_color = texture(ui_tex, uvs);
    if (ui_color.a != 0){
        f_color = ui_color;
    }
}

void alone_frag(){
    f_color = vec4(texture(tex, uvs).rgb ,1.0);
    vec2 px_uvs = vec2(floor(uvs.x * 320) / 320, floor(uvs.y * 210) / 210);
    float center_dis = distance(uvs, vec2(0.5,0.5));
    float noise_val = center_dis + texture(noise_tex1, vec2(px_uvs.x * 1.52 * 2 + itime * 0.001, px_uvs.y * 2)).r * 0.2;
    vec4 dark = vec4(0.086, 0.4549, 0.196, 1.0);
    dark = vec4(0.0, 0.0, 0.0, 1.0);
    float darkness = max(0, noise_val - 0.7) * 20;
    //float vignette = max(0, center_dis * center_dis - 0.5) * 20;
    darkness += center_dis;
    f_color = darkness * dark + (1 - darkness) * f_color;
    vec4 ui_color = texture(ui_tex, uvs);
    if (ui_color.a != 0){
        f_color = ui_color;
    }
}

void new_frag(){
    vec2 px_uvs = vec2(floor(uvs.x * 320) / 320, floor(uvs.y * 210) / 210);
    //px_uvs = vec2((floor(uvs.x * 320) + scroll_x )/320, (floor(uvs.y * 210) + scroll_y )/210);
    vec2 shiftedTexCoords = vec2(px_uvs.x + sin(time * 0.2 * time_scale ), px_uvs.y + sin(time * 0.2 * time_scale));
    vec4 noiseColor = texture(noise_tex1, shiftedTexCoords);
    shiftedTexCoords = vec2(px_uvs.x * 1.7 + sin(time * 0.5 * time_scale), px_uvs.y * 1.7 - sin(time * 0.5 * time_scale));
    vec4 noiseColor1 = texture(noise_tex1, shiftedTexCoords);
    shiftedTexCoords = vec2(px_uvs.x * 0.35 + sin(time * 0.4 * time_scale), px_uvs.y * 0.35 + sin(time * 0.4 * time_scale));
    vec4 noiseColor2 = texture(noise_tex1, shiftedTexCoords);
    vec4 combinednoiseColor = (noiseColor + noiseColor1 * 0.5 + noiseColor2 * 0.5) * 0.5;
    combinednoiseColor = combinednoiseColor * (distance(vec2(0.5,0.5), px_uvs) * 0.5 + 0.5) + sin((px_uvs.x - px_uvs.y * angle_Const) * stripeWidth) * stripeImpact;
    float center_dis = distance(uvs, vec2(0.5,0.5));
    vec4 baseColor;
    if (combinednoiseColor.r < threshold){
        baseColor = vec4(0.0, 0.0, 0.01, 1.0);
    }
    else if(combinednoiseColor.r < threshold + 0.01){
        baseColor = vec4(0.2, 0.2, 0.34, 1.0);
    }
    else if (combinednoiseColor.r < threshold + 0.05){
        baseColor = vec4(0.11, 0.118, 0.176, 1.0);
    }
    else if (combinednoiseColor.r < threshold + 0.1){
        baseColor = vec4(0.05, 0.05, 0.09, 1.0);
    }
    else{
        baseColor = vec4(0.025, 0.025, 0.045, 1.0);
    }
    f_color = baseColor;
    vec4 display_color = texture(tex, uvs);
    if (display_color.x > 0){
        f_color = display_color;
    }
    vec4 ui_color = texture(ui_tex, uvs);
    if (ui_color.a > 0){
        f_color = ui_color;
    } 
}



void main(){
    if (corrupted == 0){
        new_frag();
        overlay_frag();
    }
    else{
        alone_frag();
    }
    
}