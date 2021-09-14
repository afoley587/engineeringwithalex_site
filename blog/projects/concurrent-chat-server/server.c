
#include <stdio.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <pthread.h>

#define MAX 80
#define CHAT_PORT 8107
#define MATH_PORT CHAT_PORT+1
#define SA struct sockaddr

struct info {
  int sockfd;
};

// Function designed for chat between client and server.
void chat(void *data)
{
    struct info *info = data;
    int sockfd = info->sockfd;

    char buff[MAX];
    struct sockaddr_in chat_cli;
    int n, chat_len, chat_connfd;
    chat_len = sizeof(chat_cli);

    // infinite loop for chat
    chat_connfd = accept(sockfd, (SA*)&chat_cli, &chat_len);
    if (chat_connfd < 0) {
      printf("server accept failed...\n");
      return;
    }
    for (;;) {
        bzero(buff, MAX);
  
        // read the message from client and copy it in buffer
        read(chat_connfd, buff, sizeof(buff));
        // print buffer which contains the client contents
        printf("From client: %s\t To client : ", buff);
        if (strncmp("exit", buff, 4) == 0) {
            printf("Server Exit...\n");
            return;
        }
        bzero(buff, MAX);
        n = 0;
        // copy server message in the buffer
        while ((buff[n++] = getchar()) != '\n')
            ;
  
        // and send that buffer to client
        write(chat_connfd, buff, sizeof(buff));
        
    }
}
  
void calculator(void *data) {
    char buff[MAX];
    char *tokbuff[MAX];
    struct info *info = data;
    int sockfd = info->sockfd;

    struct sockaddr_in math_cli;
    int n, math_len, math_connfd;
    math_len = sizeof(math_cli);

    // infinite loop for chat
    math_connfd = accept(sockfd, (SA*)&math_cli, &math_len);
    if (math_connfd < 0) {
      printf("server acccept failed...\n");
      return;
    }
    // infinite loop for chat
    for (;;) {
        bzero(buff, MAX);
  
        // read the message from client and copy it in buffer
        read(math_connfd, buff, sizeof(buff));
        printf("From calculator fn: %s\n", buff);
        if (strncmp("exit", buff, 4) == 0) {
            printf("Server Exit...\n");
            break;
        }
        char *token = strtok(buff, " ");
        int i = 0;
        while( token != NULL ) {
            tokbuff[i++] = token;
            token = strtok(NULL, " ");
        }
        for (i = 0; i < 3; i++) {
          printf("BUFF: %s\n", tokbuff[i]);
        }
        char *op   = tokbuff[1];
        int first  = atoi(tokbuff[0]);
        int second = atoi(tokbuff[2]);
        int res;
        switch (*op) {
          case '+':
            res = first + second;
            break;
          case '-':
            res = first - second;
            break;
          case '*':
            res = first * second;
            break;
          case '/':
            res = first / second;
            break;
          // operator doesn't match any case constant
          default:
            printf("Error! operator is not correct");
        }

        // print buffer which contains the client contents
        bzero(buff, MAX);
        n = 0;
        // copy server message in the buffer
        sprintf(buff, "%d\n", res);
  
        // and send that buffer to client
        write(math_connfd, buff, sizeof(buff));  
    }
};

int create_socket() {
  int sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd == -1) {
    printf("socket creation failed...\n");
  }
  return sockfd;
};

void create_server(int sockfd, int port, int servaddr_size, struct sockaddr_in *servaddr) {
  servaddr->sin_family = AF_INET;
  servaddr->sin_addr.s_addr = htonl(INADDR_ANY);
  servaddr->sin_port = htons(port);

  if ((bind(sockfd, (SA*)servaddr, servaddr_size)) != 0) {
    printf("socket bind failed...\n");
    exit(0);
  }

  if ((listen(sockfd, 5)) != 0) {
    printf("Listen failed...\n");
    exit(0);
  }
};

int main()
{
  int chat_sockfd, math_sockfd;
  struct sockaddr_in chat_servaddr, math_servaddr;
  pthread_t chat_thread_id, math_thread_id;
  struct info *chat_info = malloc(sizeof(struct info));
  struct info *math_info = malloc(sizeof(struct info));

  // socket create and verification
  chat_sockfd = create_socket();
  math_sockfd = create_socket();

  if (chat_sockfd == -1 || math_sockfd == -1) {
    // socket failed
    exit(1);
  }

  bzero(&chat_servaddr, sizeof(chat_servaddr));
  bzero(&math_servaddr, sizeof(math_servaddr)); 

  create_server(chat_sockfd, CHAT_PORT, sizeof(chat_servaddr), &chat_servaddr);
  create_server(math_sockfd, MATH_PORT, sizeof(math_servaddr), &math_servaddr);

  // Function for chatting between client and server
  chat_info->sockfd = chat_sockfd;
  math_info->sockfd = math_sockfd;

  pthread_create(&chat_thread_id, NULL, chat, chat_info);
  pthread_create(&math_thread_id, NULL, calculator, math_info);
      
  pthread_join(chat_thread_id, NULL);
  pthread_join(math_thread_id, NULL);
  // After chatting close the socket
  close(chat_sockfd);
  close(math_sockfd);
}