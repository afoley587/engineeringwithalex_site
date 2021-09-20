#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#define MAX_INPUT_BUFFER 80

void read_input_to_buffer(char *buff) {
  /* Reads input from the terminal in to the buffer
   * passed in by the calling user
   */
  static int first_time = 1;
  // The ASCII Command to clear the current console
  // \033[H Moves the cursor to the top left of the screen
  // \033[J Clears the screen from the cursor to the end
  if (first_time == 1) {
    printf("\033[H\033[J");
    first_time = 0;
  }
  // Our prompt will be '>>> '
  printf(">>> ");
  // Read the line in to the buffer
  fgets(buff, MAX_INPUT_BUFFER, stdin);
  //replace the newline with a null character to terminate the array
  buff[strcspn(buff, "\n")] = 0;
};

void parse_command(char *raw_buff[], char *command[], char *params[]) {
  /* Parses the input from the terminal into a command buffer
   * and the params buffer
   * For example: 
   * If the raw_buff is ['/bin/ls -larth /foo/bar'], then
   * command = ['/bin/ls'] and params = ['/bin/ls', '-larth', '/foo/bar']
   */
  int token_num = 0;
  char *arr[MAX_INPUT_BUFFER];
  char *token = strtok(raw_buff, " ");
  int i = 0;

  // Tokenize the space separated string into 
  // the arr array
  while( token != NULL ) {
    arr[i++] = strdup(token);
    token_num++;
    token = strtok(NULL, " ");
  }

  command[0] = strdup(arr[0]);
  for (i = 0; i < token_num; i++) {
    params[i] = strdup(arr[i]);
  }
};

int main() {
  char buffer[MAX_INPUT_BUFFER], *command[MAX_INPUT_BUFFER], *params[MAX_INPUT_BUFFER];
  char *envp[MAX_INPUT_BUFFER]  = { (char *) "PATH=/bin:/usr/bin:/usr/sbin", (char*)0};

  for (;;) {
    // Zero out all array so no lingering data
    bzero(buffer, MAX_INPUT_BUFFER);
    bzero(command, MAX_INPUT_BUFFER);
    bzero(params, MAX_INPUT_BUFFER);
    // Read the terminal input in to the buffer
    read_input_to_buffer(&buffer);
    // Parse the raw string in to tokens
    parse_command(&buffer, &command, &params);

    // if the user requests an exit, exit gracefully
    if (strcmp(command[0], "exit") == 0) {
      printf("EXITING!\n");
      exit(0);
    }
    // Create the child process
    if ( fork() != 0 ) {
      // Wait for the child process to finish
      wait(NULL);
    } else {
      if (execve(command[0], params, envp) == -1) {
        perror("Could not execve!");
        // exit child process
        exit(1);
      }
    }
  }
  return 0;
}