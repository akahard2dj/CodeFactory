// glfw_test.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>

#include <gl/glew.h>
#include <GLFW/glfw3.h>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include "shader.h"
#include "draw_vertex.h"

#include <SOIL/SOIL.h>

glm::vec3 camera_pos = glm::vec3(0.0f, 0.0f, 3.0f);
glm::vec3 camera_front = glm::vec3(0.0f, 0.0f, -1.0f);
glm::vec3 camera_norm = glm::vec3(0.0f, 1.0f, 0.0f);

GLfloat angle_yaw = -90.0f;
GLfloat angle_pitch = 0.0f;
GLfloat last_x = 0.0f;
GLfloat last_y = 0.0f;

GLfloat fov = 45.0f;
GLfloat dt = 0.0f;
GLfloat last_frame = 0.0f;
bool keys[1024];
bool isClick = false;

void glfw_init(int major, int minor)
{
	std::cout << "Starting GLFW context, OpenGL 3.3" << std::endl;
	glfwInit();
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, major);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, minor);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
}

GLFWwindow *create_glfw_window(int width, int height, const char *window_name)
{
	GLFWwindow *window = glfwCreateWindow(width, height, window_name, nullptr, nullptr);
	if (window == nullptr) {
		std::cout << "Failed to create GLFW window" << std::endl;
		glfwTerminate();
		exit(EXIT_FAILURE);
	}

	return window;
}

void glew_init()
{
	glewExperimental = GL_TRUE;
	if (glewInit() != GLEW_OK) {
		std::cout << "Failed to initializing GLEW" << std::endl;
		glfwTerminate();
		exit(EXIT_FAILURE);
	}
}

void do_movement()
{
	GLfloat camera_speed = 5.0f * dt;
	if (keys[GLFW_KEY_W])
		camera_pos += camera_speed * camera_front;
	if (keys[GLFW_KEY_S])
		camera_pos -= camera_speed * camera_front;
	if (keys[GLFW_KEY_A])
		camera_pos -= glm::normalize(glm::cross(camera_front, camera_norm)) * camera_speed;
	if (keys[GLFW_KEY_D])
		camera_pos += glm::normalize(glm::cross(camera_front, camera_norm)) * camera_speed;
	if (keys[GLFW_KEY_R]) {
		camera_pos = glm::vec3(0.0f, 0.0f, 3.0f);
		camera_front = glm::vec3(0.0f, 0.0f, -1.0f);
		camera_norm = glm::vec3(0.0f, 1.0f, 0.0f);
	}

}

void key_callback(GLFWwindow* window, int key, int scancode, int action, int mode)
{
	if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
		glfwSetWindowShouldClose(window, GL_TRUE);
	if (key >= 0 && key < 1024) {
		if (action == GLFW_PRESS)
			keys[key] = true;
		else if (action == GLFW_RELEASE)
			keys[key] = false;
	}
}

void cursorpos_callback(GLFWwindow *window, double xpos, double ypos)
{
	if (isClick) {
		
		GLfloat xoffset = (xpos - last_x) / 30.0;
		GLfloat yoffset = (ypos - last_y) / 30.0;

		GLfloat sensitivity = 0.005f;
		xoffset += sensitivity;
		yoffset += sensitivity;
		std::cout << xoffset << ", " << yoffset << std::endl;

		angle_yaw += xoffset;
		angle_pitch += yoffset;

		if (angle_pitch > 89.0f)
			angle_pitch = 89.0f;
		if (angle_pitch < -89.0f)
			angle_pitch = -89.0f;

		glm::vec3 front;
		front.x = cos(glm::radians(angle_yaw)) * cos(glm::radians(angle_pitch));
		front.y = sin(glm::radians(angle_pitch));
		front.z = sin(glm::radians(angle_yaw)) * cos(glm::radians(angle_pitch));
		camera_front = glm::normalize(front);
	}
	last_x = xpos;
	last_y = ypos;
}

void mousebutton_callback(GLFWwindow *window, int button, int action, int mods)
{
	if (button == GLFW_MOUSE_BUTTON_LEFT && action == GLFW_PRESS)
		isClick = true;
	else if (button == GLFW_MOUSE_BUTTON_LEFT && action == GLFW_RELEASE)
		isClick = false;
		
}

void scroll_callback(GLFWwindow *window, double xoffset, double yoffset)
{
	std::cout << fov << ", " << yoffset << std::endl;
	if (fov >= 1.0f && fov <= 45.0f)
		fov -= (yoffset/10.0);
	if (fov <= 1.0f)
		fov = 1.0f;
	if (fov >= 45.0f)
		fov = 45.0f;
}

int _tmain(int argc, _TCHAR* argv[])
{
	glfw_init(3, 3);
	GLFWwindow *window = create_glfw_window(800, 600, "OpenGL 3.3");
	glfwMakeContextCurrent(window);
	glfwSetKeyCallback(window, key_callback);
	glfwSetScrollCallback(window, scroll_callback);
	glfwSetCursorPosCallback(window, cursorpos_callback);
	glfwSetMouseButtonCallback(window, mousebutton_callback);
	glew_init();

	glViewport(0, 0, 800, 600);

	// Build and compile our shader program
	Shader ourShader("./shader.vert", "./shader.frag");

	DrawVertex drawElement;
	drawElement.bind();

	// Load and create a texture 
	GLuint texture;
	glGenTextures(1, &texture);
	glBindTexture(GL_TEXTURE_2D, texture); // All upcoming GL_TEXTURE_2D operations now have effect on this texture object
	// Set the texture wrapping parameters
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);	// Set texture wrapping to GL_REPEAT (usually basic wrapping method)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
	// Set texture filtering parameters
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	// Load image, create texture and generate mipmaps
	int width, height;
	unsigned char* image = SOIL_load_image("container.jpg", &width, &height, 0, SOIL_LOAD_RGB);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image);
	glGenerateMipmap(GL_TEXTURE_2D);
	SOIL_free_image_data(image);
	glBindTexture(GL_TEXTURE_2D, 0); // Unbind texture when done, so we won't accidentily mess up our texture.


	while (!glfwWindowShouldClose(window)) {
		GLfloat current_frame = glfwGetTime();
		dt = current_frame - last_frame;
		last_frame = current_frame;

		glfwPollEvents();

		do_movement();
		
		glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
		glClear(GL_COLOR_BUFFER_BIT);

		glBindTexture(GL_TEXTURE_2D, texture);

		// Activate shader
		ourShader.Use();

		glm::mat4 model;
		glm::mat4 view;
		glm::mat4 projection;

		//model = glm::rotate(model, -25.0f, glm::vec3(1.0f, 0.0f, 0.0f));
		//view = glm::translate(view, glm::vec3(0.0f, 0.0f, -3.0f));
		//projection = glm::perspective(45.0f, (GLfloat)800 / (GLfloat)600, 0.1f, 100.0f);

		view = glm::lookAt(camera_pos, camera_pos + camera_front, camera_norm);
		projection = glm::perspective(80.0f, (GLfloat)800 / (GLfloat)600, 0.1f, 100.0f);

		GLint modelLoc = glGetUniformLocation(ourShader.Program, "model");
		GLint viewLoc = glGetUniformLocation(ourShader.Program, "view");
		GLint projLoc = glGetUniformLocation(ourShader.Program, "projection");

		glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm::value_ptr(model));
		glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm::value_ptr(view));
		glUniformMatrix4fv(projLoc, 1, GL_FALSE, glm::value_ptr(projection));
		
		// Draw container
		drawElement.draw();

		// Swap the screen buffers
		glfwSwapBuffers(window);
	}

	drawElement.unbind();

	glfwTerminate();
	return 0;
}

