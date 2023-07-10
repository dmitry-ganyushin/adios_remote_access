#define _XOPEN_SOURCE 700
#include <arpa/inet.h>
#include <assert.h>
#include <netdb.h> /* getprotobyname */
#include <netinet/in.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <netinet/in.h>
#include <netinet/tcp.h>

int main(int argc, char** argv) {
  char buffer[BUFSIZ];
  enum CONSTEXPR { MAX_REQUEST_LEN = 1024 };
  char request[MAX_REQUEST_LEN];
  char request_template[] =
      "GET /%s HTTP/1.1\r\nHost: %s\r\nRange: bytes=%d-%d\nConnection: keep-alive\nKeep-Alive: timeout=5, max=100\r\n\r\n";
  struct protoent *protoent;
  char *hostname;
  in_addr_t in_addr;
  int request_len;
  int socket_file_descriptor;
  ssize_t nbytes_total, nbytes_last;
  struct hostent *hostent;
  struct sockaddr_in sockaddr_in;
  unsigned short server_port = 80;
  int start_byte = 0;
  int end_byte = 100;
  char path[] = "/home/ganyush/adiostests/test.bp/md.idx";

  if (argc > 1)
    hostname = argv[1];
  if (argc > 2) {
    server_port = strtoul(argv[2], NULL, 10);
  }

  request_len = snprintf(request, MAX_REQUEST_LEN, request_template, path,
                         hostname, start_byte, end_byte);
  if (request_len >= MAX_REQUEST_LEN) {
    fprintf(stderr, "request length large: %d\n", request_len);
    exit(EXIT_FAILURE);
  }

  /* Build the socket. */
  protoent = getprotobyname("tcp");
  if (protoent == NULL) {
    perror("getprotobyname");
    exit(EXIT_FAILURE);
  }
  socket_file_descriptor = socket(AF_INET, SOCK_STREAM, protoent->p_proto);
  if (socket_file_descriptor == -1) {
    perror("socket");
    exit(EXIT_FAILURE);
  }
/*
 * HTTPConnection.default_socket_options += [
  (socket.SOL_SOCKET, socket.SO_KEEPALIVE,1),
  (socket.IPPROTO_TCP, socket.TCP_KEEPIDLE ,60),
  (socket.IPPROTO_TCP,socket.TCP_KEEPINTVL,60),
  (socket.IPPROTO_TCP,socket.TCP_KEEPCNT,100),
  ]
 */
  /* set socket options */
  int opt_val = 1;
  if ( setsockopt ( socket_file_descriptor , SOL_SOCKET , SO_KEEPALIVE , ( char* ) &opt_val , sizeof ( int ) ) < 0 )
  {
    perror ( " error setting socket " ) ;
    exit ( 0 ) ;
  }
  opt_val = 60;
  if ( setsockopt ( socket_file_descriptor , IPPROTO_TCP , TCP_KEEPIDLE , ( char* ) &opt_val , sizeof ( int ) ) < 0 )
  {
    perror ( " error setting socket " ) ;
    exit ( 0 ) ;
  }
  opt_val = 60;
  if ( setsockopt ( socket_file_descriptor , IPPROTO_TCP , TCP_KEEPINTVL , ( char* ) &opt_val , sizeof ( int ) ) < 0 )
  {
    perror ( " error setting socket " ) ;
    exit ( 0 ) ;
  }
  opt_val = 100;
  if ( setsockopt ( socket_file_descriptor , IPPROTO_TCP , TCP_KEEPCNT , ( char* ) &opt_val , sizeof ( int ) ) < 0 )
  {
    perror ( " error setting socket " ) ;
    exit ( 0 ) ;
  }

  /* Build the address. */
  hostent = gethostbyname(hostname);
  if (hostent == NULL) {
    fprintf(stderr, "error: gethostbyname(\"%s\")\n", hostname);
    exit(EXIT_FAILURE);
  }
  in_addr = inet_addr(inet_ntoa(*(struct in_addr *)*(hostent->h_addr_list)));
  if (in_addr == (in_addr_t)-1) {
    fprintf(stderr, "error: inet_addr(\"%s\")\n", *(hostent->h_addr_list));
    exit(EXIT_FAILURE);
  }
  sockaddr_in.sin_addr.s_addr = in_addr;
  sockaddr_in.sin_family = AF_INET;
  sockaddr_in.sin_port = htons(server_port);

  /* Actually connect. */
  if (connect(socket_file_descriptor, (struct sockaddr *)&sockaddr_in,
              sizeof(sockaddr_in)) == -1) {
    perror("connect");
    exit(EXIT_FAILURE);
  }
  for (int i = 0; i < 10; i++) {
    printf("%d:  Attempt \n", i);
    /* Send HTTP request. */
    nbytes_total = 0;
    while (nbytes_total < request_len) {
      nbytes_last = write(socket_file_descriptor, request + nbytes_total,
                          request_len - nbytes_total);
      if (nbytes_last == -1) {
        perror("write");
        exit(EXIT_FAILURE);
      }
      nbytes_total += nbytes_last;
    }
    printf("%d: Send GET \n", i);
    /* Read the response. */
    fprintf(stderr, "debug: %d before first read\n", i);
    while ((nbytes_total = read(socket_file_descriptor, buffer, BUFSIZ)) > 0) {
      fprintf(stderr, "debug: after a read\n");
      //write(STDOUT_FILENO, buffer, nbytes_total);
    }
    fprintf(stderr, "debug: %d after last read\n", i);
    if (nbytes_total == -1) {
      perror("error read");
      exit(EXIT_FAILURE);
    }
  }
 //   sleep(1000);
    close(socket_file_descriptor);
    exit(EXIT_SUCCESS);
}
