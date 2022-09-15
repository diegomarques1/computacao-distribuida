// Diego Souza Lima Marques - TIA: 32039921
// Lucas de Camargo Gonçalves - TIA: 32074964
// Computação Distribuída - 06D
// Versão paralela com MPI do projeto de Computação Paralela

#include "mpi.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char* argv[]) 
{
  double soma_parcial = 0, soma = 0, local_n, i, inicio, fim, d;
  double ln = 1000;
  double data, my_data;
  double res_receiv;
  int myid, numprocs; 
  // nessa implementação, numprocs precisa ser um número divisor de ln.
  // exemplo: ln = 10 -> 10 % 1 = 0 e 10 % 2 = 0 -> OK
  // 10 % 3 = 1 e 10 % 4 = 2, logo, não vai ter o resultado esperado

  MPI_Init(NULL, NULL);
  MPI_Comm_size(MPI_COMM_WORLD,&numprocs);
  MPI_Comm_rank(MPI_COMM_WORLD,&myid);
  
  local_n = ln/numprocs;

  if (myid == 0)
  {
    for (i = 1; i < numprocs; i++)
    {
      inicio = local_n*i + 1; 
      MPI_Send(&inicio, 1, MPI_DOUBLE, i, 0, MPI_COMM_WORLD);
    }
  }
  else
  {
    MPI_Recv(&my_data, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
  }
  
  if (myid == 0)
  {
    inicio = local_n*myid + 1; 
    fim = inicio + local_n - 1;
    for (d = inicio; d <= fim; d++)
    {
      soma_parcial += 1/d; // soma interna do processo 0
    }
  }
  else
  {
    fim = my_data + local_n - 1;
    for (d = my_data; d <= fim; d++)
    {
      soma_parcial += 1/d; // soma interna dos outros processos
    }
    MPI_Send(&soma_parcial, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
  }
 
  
  if (myid == 0)
  {
    soma = soma_parcial;
    for (i = 1; i < numprocs; i++)
    {
      MPI_Recv(&res_receiv, 1, MPI_DOUBLE, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      soma += res_receiv;
    }
    printf("\nln(%d) = %f\n", (int) ln, soma);
  }

  MPI_Finalize(); // talvez precise mudar de linha
  return 0;
}