#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#define MAX_INPUT_BUFFER 80

void read_input_to_buffer(char *buff) {
  static int first_time = 1;
  if (first_time == 1) {
    printf("\033[H\033[J");
    first_time = 0;
  }
  printf(">>> ");
  fgets(buff, MAX_INPUT_BUFFER, stdin);
  buff[strcspn(buff, "\n")] = 0;
};

void parse_command(char *raw_buff[], char *command[], char *params[]) {
  int token_num = 0;
  char *arr[MAX_INPUT_BUFFER];
  char *token = strtok(raw_buff, " ");
  int i = 0;

  while( token != NULL ) {
    arr[i++] = strdup(token);
    token_num++;
    token = strtok(NULL, " ");
  }
  printf("BEFORE COMAND\n");
  command[0] = strdup(arr[0]);
  command[1] =  (char*)0;
  printf("COMMAND[i] = %s\n", command[0]);

  for (i = 0; i < token_num; i++) {
    params[i] = strdup(arr[i]);
    printf("PARAM[i] = %s\n", params[i-1]);
  }
};

int main() {
  char buffer[MAX_INPUT_BUFFER], *command[MAX_INPUT_BUFFER], *params[MAX_INPUT_BUFFER];
  char *envp[MAX_INPUT_BUFFER]  = { (char *) "PATH=/bin:/usr/bin:/usr/sbin", (char*)0};
  char *cbuff[MAX_INPUT_BUFFER] = { "/bin/ls", (char*)0};
  char *cpams[MAX_INPUT_BUFFER] = { "/bin/ls", "/Users/alex/Projects/SRE-487/jenkins-jobs", (char*)0};

  for (;;) {
    bzero(buffer, MAX_INPUT_BUFFER);
    bzero(command, MAX_INPUT_BUFFER);
    bzero(params, MAX_INPUT_BUFFER);
    read_input_to_buffer(&buffer);
    parse_command(&buffer, &command, &params);
    printf("BACK\n");
    printf("COMMAND: %s\n", command[0]);
    for (int i = 0; i < 1; i++) {
      printf("PARAM: %s\n", params[i]);
    }
    if ( fork() != 0 ) {
      wait(NULL);
    } else {
      printf("EXEC!\n");
      if (execve(command[0], params, envp) == -1) {
        perror("Could not execve!");
      }
    }

    if (strcmp(command[0], "exit") == 0) {
      printf("EXITING!\n");
      exit(0);
    }
    
  }
  return 0;
}