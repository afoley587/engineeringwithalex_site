
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

// Super simple struct to hold the socket file descriptor
struct info {
  int sockfd;
};

void chat(void *data)
{
    /* A simple chat server which just reads data from a buffer
     * and writes data to the buffer.
     * Arguments:
     *    data - Void pointer which holds a "info" object defined above
     */
    
    char buff[MAX];
    struct sockaddr_in chat_cli;
    int n, chat_connfd;
    struct info *info = data;
    int sockfd        = info->sockfd;
    int chat_len      = sizeof(chat_cli);

    // Accept the client connections
    chat_connfd = accept(sockfd, (SA*)&chat_cli, &chat_len);
    if (chat_connfd < 0) {
      printf("server accept failed...\n");
      return;
    }

    // Infinite loop
    for (;;) {
        // Remove the data from the buffer by zeroing it out
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
    /* Acts as an extremely simple calculator that expects
     * data.
     */
    char buff[MAX];
    char *tokbuff[MAX];
    struct sockaddr_in math_cli;
    int math_connfd;

    struct info *info = data;
    int sockfd        = info->sockfd;
    int math_len      = sizeof(math_cli);

    // Accept the client connections
    math_connfd = accept(sockfd, (SA*)&math_cli, &math_len);
    if (math_connfd < 0) {
      printf("server acccept failed...\n");
      return;
    }

    // infinite loop
    for (;;) {

        // Zero the buffer
        bzero(buff, MAX);
  
        // Remove the data from the buffer by zeroing it out
        read(math_connfd, buff, sizeof(buff));
        printf("From calculator fn: %s\n", buff);
        if (strncmp("exit", buff, 4) == 0) {
            printf("Server Exit...\n");
            break;
        }

        // Tokenize the space delimited string
        char *token = strtok(buff, " ");
        int i = 0;
        while( token != NULL ) {
            // Create the token buffer array for ease of access later
            tokbuff[i++] = strdup(token);
            token = strtok(NULL, " ");
        }

        char *op    = tokbuff[1];
        int first   = atoi(tokbuff[0]);
        int second  = atoi(tokbuff[2]);
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

        // copy server message in the buffer
        sprintf(buff, "%d\n", res);
  
        // and send that buffer to client
        write(math_connfd, buff, sizeof(buff));  
    }
};

int create_socket() {
  /* Creates a socket connection and returns the file
   * descriptor of that socket.
   * 
   * Arguments:
   *    None
   * Returns:
   *    sockfd - The file descriptor of the opened socket
   */
  int sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd == -1) {
    printf("socket creation failed...\n");
  }
  return sockfd;
};

void create_server(int sockfd, int port, 
                   int servaddr_size, struct sockaddr_in *servaddr) {
  /* Creates a server with the given socket,
   * on the given address and port.
   * 
   * Arguments:
   *    sockfd        - Socket File Descriptor that the server should bind to
   *    port          - The port to listen on
   *    servaddr_size - The size of the servaddr
   *    servaddr      - Pointer to the servaddr object. Will be used to bind 
   *                    the socket to the requested address
   * Returns:
   *    None
   */

  // Set the address and port to listen on
  servaddr->sin_family = AF_INET;
  // Bind to unspecified address so it can listen on 0.0.0.0
  servaddr->sin_addr.s_addr = htonl(INADDR_ANY);
  servaddr->sin_port = htons(port);

  // Bind the socket file descriptor to the address defined above
  // so the socket can listen at that address
  if ((bind(sockfd, (SA*)servaddr, servaddr_size)) != 0) {
    printf("socket bind failed...\n");
    exit(0);
  }


  // Begin listening on that socket
  if ((listen(sockfd, 5)) != 0) {
    printf("Listen failed...\n");
    exit(0);
  }
};

int main()
{
  /* This script will open a few sockets on the running machine
   * which you can connect to with a client
   * One port will be opened as a "chat" server where the 
   * client can send messages to the server and the server
   * can respond. The other port will act as a simple
   * calculator.
   */
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

  // Initialize the chat server and math server sockaddr_in
  // to reduce garbage / uninitialized items
  bzero(&chat_servaddr, sizeof(chat_servaddr));
  bzero(&math_servaddr, sizeof(math_servaddr)); 

  // Create the servers
  create_server(chat_sockfd, CHAT_PORT, sizeof(chat_servaddr), &chat_servaddr);
  create_server(math_sockfd, MATH_PORT, sizeof(math_servaddr), &math_servaddr);

  // Function for chatting between client and server
  chat_info->sockfd = chat_sockfd;
  math_info->sockfd = math_sockfd;

  // Create threads to run the server applications
  pthread_create(&chat_thread_id, NULL, chat, chat_info);
  pthread_create(&math_thread_id, NULL, calculator, math_info);
      
  // Wait for the applications to exit
  pthread_join(chat_thread_id, NULL);
  pthread_join(math_thread_id, NULL);

  // Close the sockets
  close(chat_sockfd);
  close(math_sockfd);
}