typedef struct graph{
        int size;
        int** data;
}graph;

void init(graph*);
void display_graph(graph*);
void display_degree(graph*);
int check_connectivity(graph*);
void display_components(graph*);
int isadjacent(graph*, int, int);



GRAPH.C


#include<stdio.h>
#include<stdlib.h>
#include"graph.h"


void init(graph* g){

    FILE *fp;
    int **matrix;
    int n;
    int i, j;

    char filename[50];
    printf("Enter the filename with the matrix : ");
    scanf("%s", filename);

    // Open file for reading
    fp = fopen(filename, "r");
    if (fp == NULL) {
        printf("Error opening file!\n");
    }

    // Read the number of columns from the file
    fscanf(fp, "%d", &n);

    // Allocate memory for the matrix
    matrix = (int **)malloc(n * sizeof(int *));
    if (matrix == NULL) {
        printf("Memory allocation failed!\n");
        return;
    }

    for (i = 0; i < n; i++) {
        matrix[i] = (int *)malloc(n * sizeof(int));
        if (matrix[i] == NULL) {
            printf("Memory allocation failed!\n");
            return;
        }
    }

    // Read the matrix elements
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            fscanf(fp, "%d", &matrix[i][j]);
        }
    }

    // Close the file
    fclose(fp);

    g->size = n;
    g->data = matrix;

    return;

}

void display_graph(graph *g){
    int n = g->size;

    for(int i = 0; i < n; i++){
        for(int j = 0; j < n; j++){
            printf("%d ",g->data[i][j]);
        }
        printf("\n");
    }
}

void display_degree(graph *g){
    int n = g->size;
    for(int i = 0; i < n; i++){
        int degree = 0;
        for(int j = 0; j < n; j++){
            if(g->data[i][j] == 1){
                degree++;
            }
        }
        printf("degree of vertex %d : %d", i, degree);
        printf("\n");
    }
    return;
}

int check_connectivity(graph* g){
    int i,j,n;
    
    n = g->size;
    int a[n];

    // initializing whole array to first element
    for(j = 0; j < n; j++){
        a[j] = g->data[0][j];
        if(a[j]){
            a[0] = 1; // conveys that a is connected to others
        }
    }

    for(i = 0; i < n; i++){
        for(j = 0; j < n; j++){
            if(a[i]){
                if(g->data[i][j]){
                    a[j] = 1;
                }
            }
            
        }
    }

    for(i = 0; i < n; i++){
        if(!a[i]){
            // printf("The Graph is not connected");
            return 0;
        }
    }

    // printf("The graph is connected");
    return 1;
}


void display_components(graph* g){
    int i,j,k,n;
    
    n = g->size;
    int a[n];

    for(k = 0; k < n; k++){

        // initializing whole array to component element
        for(j = 0; j < n; j++){
            a[j] = g->data[k][j];
            if(a[j]){
                a[k] = 1; // conveys that the component is connected to others
            }
        }

        for(i = 0; i < n; i++){
            for(j = 0; j < n; j++){
                if(a[i]){
                    if(g->data[i][j]){
                        a[j] = 1;
                    }
                }
                
            }
        }
        printf("Component %d : ", k);
        for(i = 0; i < n; i++){
            if(a[i]){
                printf("%d ", i);   
            }
        }
        printf("\n");

    }
    return;
}


int isadjacent(graph* g, int i, int j){
    if(g->data[i][j]){
        return 1;
    }
    return 0;
}



MAIN.C

#include<stdio.h>
#include<stdlib.h>
#include"graph.c"

int main() {

    graph g;
    init(&g);

    display_graph(&g);
    display_degree(&g);
    int c = check_connectivity(&g);

    if(c){
        printf("The graph is connected\n");
    }
    else{
        printf("The graph is not connected\n");
    }

    display_components(&g);

    printf("Enter two vertices to check adjacency :");
    int i, j;
    scanf("%d %d", &i, &j);
    int adj = isadjacent(&g, i, j);
    if(adj){
        printf("The given vertices are adjacent");
    }
    else{
        printf("The given vertices are not adjacent");
    }



    printf("\n");
    return 0;
    

}
