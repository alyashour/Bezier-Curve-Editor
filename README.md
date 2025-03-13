# OpenGL Bezier Curve Editor

## How to use

First install the required packages in `requirements.txt`.
Then run the app by running 

```bash
python main.py <window_width> <window_height>
```

## Components

The assignment is split into an engine half and an app half.  
The engine half handles the window, rendering, and input management.  
The app half contains all the parts of the assignment. The spline, the control points, the nodes, drawing, etc.

### Engine

The app class has the highest level of control during runtime.  

It's initialization creates the window. It also has ownership of the input manager and the renderer.  

Running the app enters the app into a standard glfw main loop. The renderer is told to clear, buffers are swapped, and the app is allowed to draw to the buffer.  

The input manager, renderer, and window classes each handle input, rendering (and drawing), and window openGL and glfw api calls respectively. I've commented as much as possible and I believe the code is relatively readable so please see those files for more details.

### App
The app half contains the concrete implementation of the abstract app class from the engine as well as app specific classes like spline, control point, and node classes.

Some notes about the code:

> **Control point positions are actually stored as relative to their respective node in memory.**
>
> At first glance this may seem to complicate the code but really it means many of the operations like moving nodes/control points, calculating the colinear control point's position, and others is much simpler.
>
> For example, when moving nodes their respective control points must also move with them. If the control points were saved in absolute coordinates both control points would have to be updated when the central node moved but because the control points' positions are relative all that needed to change were the central node's coordinates.
>
> Secondly, to calculate the other control point's position given the current one we can simple negate its vector. I.e., the vector towards control point 1, $v_1$ is always equal to $-v_2$.

>**App windows use the framebuffer size instead of the window size**
> 
> This is because on HDPI displays like mine the framebuffer size and the input window size are not actually the same. In my case the framebuffer is 4x as big as the input dimensions as every window pixel in length is actually 2 pixels on my monitor.

# Thanks!
Aly Ashour  