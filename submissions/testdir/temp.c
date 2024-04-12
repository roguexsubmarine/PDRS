#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include "graph.h"

void initGraph(graph* G, char* fileName) {
    FILE *fp;
    fp = fopen(fileName , "r");
    fscanf(fp, "%d", &G->size);
    G->node = (int **)malloc(sizeof(int*) * G->size);
    for (int i = 0 ; i < G->size ; i++) {
        G->node[i] = (int *)malloc(sizeof(int) * G->size);
        for (int j = 0 ; j < G->size ; j++) {
            fscanf(fp, "%d", &G->node[i][j]);    
        } 
    }
}   

void displayGraph(graph* G) {
    printf("The adjacency Matrix of the Graph is as follows: \n");
    for(int i = 0 ; i < G->size ; i++) {
        for(int j = 0 ; j < G->size ; j++) {
            printf("%d ", G->node[i][j]);
        }
        printf("\n");
    }
}

int isAdjacent(graph* G,int vertex1, int vertex2) {
    if(!G) {
        return 0;
    }
    if(G->node[vertex1][vertex2] != 0) {
        return 1;
    } else {
        return 0;
    }
}

int getDegree(graph* G,int vertex) {
    int degree = 0;
    for(int i = 0 ; i < G->size ; i++) {
        if(G->node[vertex][i] != 0) {
            degree++;
        }
    }
    return degree;
}

int dfs(graph* G, int vertex, int* visited) {
    visited[vertex] = 1;
    int numVertices = 1;
    for(int i = 0; i < G->size ; i++) {
        if(G->node[vertex][i] != 0 && !visited[i]) {
            numVertices += dfs(G, i ,visited);
        }
    }
    return numVertices;
}

int isConnected(graph* G) {
    int* visited;
    visited = (int *)malloc(sizeof(int) * G->size);
    for(int i = 0 ; i < G->size ; i++){
        visited[i] = 0;                     // initilize each vertex as not visited initially    
    }
    dfs(G, 0, visited);
    for(int i = 0; i< G->size; i++) {
        if(!visited[i]) {
            return 0;
        }
    }
    return 1;
}

int getComponents(graph* G, int* numComponents){
    int count = 0;
    int* visited;
    visited = (int *)malloc(sizeof(int) * G->size);
    for (int i = 0; i < G->size; i++) {
        visited[i] = 0;
    }
    for (int i = 0; i < G->size; i++) {
        if (!visited[i]) {
            int numVertices = dfs(G, i, visited);     // number of vertices in each component
            numComponents[count] = numVertices;        
            count++;
        }
    }
    return count;
}

#include <stdio.h>
#include <stdlib.h>

typedef struct graph {
    int size;
    int **node;                                     // The 2-D adjacency matrix              
}graph;

void initGraph(graph* , char* );
void displayGraph(graph* );
int isAdjacent(graph* , int ,int);
int getDegree(graph* ,int );
int isConnected(graph* );
int getComponents(graph* ,int* ); 
// Traversal
int dfs(graph* , int , int* );
