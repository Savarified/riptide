import org.lwjgl.glfw.GLFW;
import org.lwjgl.opengl.GL;
import org.lwjgl.opengl.GL11;

public class Main {

    public static void main(String[] args) {
        // Initialize GLFW
        if (!GLFW.glfwInit()) {
            System.err.println("GLFW initialization failed!");
            System.exit(1);
        }

        // Create a windowed mode window and its OpenGL context
        long window = GLFW.glfwCreateWindow(800, 600, "Set Pixel to Red", 0, 0);
        if (window == 0) {
            System.err.println("Failed to create the GLFW window!");
            System.exit(1);
        }

        // Make the OpenGL context current
        GLFW.glfwMakeContextCurrent(window);
        GLFW.glfwSwapInterval(1); // Enable v-sync
        GL.createCapabilities(); // Initialize OpenGL

        // Set the clear color to white (default background color)
        GL11.glClearColor(1.0f, 1.0f, 1.0f, 1.0f); // White background
        GL11.glClear(GL11.GL_COLOR_BUFFER_BIT); // Clear the screen

        // Set up the pixel color to red
        GL11.glColor3f(1.0f, 0.0f, 0.0f); // Red color (R, G, B)

        // Set the pixel at the center of the window (400, 300)
        GL11.glBegin(GL11.GL_POINTS); // Start drawing points
        GL11.glVertex2f(0.0f, 0.0f); // Coordinates of the pixel, centered at (0, 0)
        GL11.glEnd();

        // Main render loop
        while (!GLFW.glfwWindowShouldClose(window)) {
            // Poll events
            GLFW.glfwPollEvents();

            // Swap buffers
            GLFW.glfwSwapBuffers(window);
        }

        // Clean up and terminate
        GLFW.glfwDestroyWindow(window);
        GLFW.glfwTerminate();
    }
}