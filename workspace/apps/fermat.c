#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <inttypes.h>
#include <mpi.h>
#include <assert.h>

#define true 1
#define false 0

typedef unsigned long long uLong;
typedef int bool;

// 64-bit pseudonumber generator
//---------------------------------
uLong getRand(uLong a, uLong b)
{
    uLong w;
    int i;

    for (i = 1; i <= 8; i++)
    {
        w <<= 8;           //left shift
        w &= rand() % 256; //logic AND
    }
    return a + (w % (b - a));
}

// Function computes greatest common divisor
//--------------------
uLong gcd(uLong a, uLong b)
{
    uLong buffer;

    while (b)
    {
        buffer = b;
        b = a % b;
        a = buffer;
    }
    return a;
}

// Function multiplies a and b mod n
//--------------------------
uLong multipyModulo(uLong a, uLong b, uLong n)
{
    uLong mask, result;

    result = 0;
    for (mask = 1; mask; mask <<= 1)
    {
        if (b & mask)
            result = (result + a) % n;
        a = (a << 1) % n;
    }
    return result;
}

// Function computes a^e mod n
//--------------------------
uLong compoundModulo(uLong a, uLong e, uLong n)
{
    uLong mask, p, result;

    p = a;
    result = 1;
    for (mask = 1; mask; mask <<= 1)
    {
        if (e & mask)
            result = multipyModulo(result, p, n);
        p = multipyModulo(p, p, n);
    }
    return result;
}

// Array of first 169 prime numbers
//------------------------------------------
const uLong primeNumbers[] = {
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
    71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163,
    167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269,
    271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383,
    389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
    503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619,
    631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751,
    757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881,
    883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009};

bool checkNumber(uLong testedNumber, uLong *baseTable, int tableSize)
{
    bool isPrime = true;
    uLong base;
    int i;

    if (testedNumber > 1009)
    {
        for (i = 0; i < tableSize; i++)
        {
            base = baseTable[i];
            if ((gcd(testedNumber, base) != 1) || (compoundModulo(base, testedNumber - 1, testedNumber) != 1))
            {
                isPrime = false;
                break;
            }
        }
    }

    return isPrime;
}

int main(int argc, char *argv[])
{

    if (argc != 2)
    {
        printf("Bledna liczba argumentow\n");
        exit(-1);
    }

    int EXIT_CODE = 1;
    uLong testedNumber, *baseTable = NULL, *subBaseTable = NULL;
    int i; //iterator

    bool isPrime = true;
    bool *results = NULL;

    srand((unsigned)time(NULL));

    MPI_Init(&argc, &argv);

    int processNumber;
    MPI_Comm_rank(MPI_COMM_WORLD, &processNumber);
    int numberOfProcesses;
    MPI_Comm_size(MPI_COMM_WORLD, &numberOfProcesses);

    testedNumber = strtoull(argv[1], NULL, 10);

    for (i = 0; i < 169; i++)
    {
        if ((testedNumber != primeNumbers[i]) && (testedNumber % primeNumbers[i] == 0))
        {
            isPrime = false;
            break;
        }
    }

    if (isPrime && testedNumber > 1009)
    {
        if (processNumber == 0)
        {

            baseTable = (uLong *)calloc(numberOfProcesses * 10, sizeof(uLong));
            assert(baseTable != NULL);

            for (i = 0; i < numberOfProcesses * 10; i++)
            {
                baseTable[i] = getRand(2, testedNumber - 1);
            }
        }

        MPI_Barrier(MPI_COMM_WORLD);
        subBaseTable = (uLong *)calloc(10, sizeof(uLong));
        assert(subBaseTable != NULL);

        MPI_Scatter(baseTable, 10, MPI_UNSIGNED_LONG_LONG, subBaseTable, 10, MPI_UNSIGNED_LONG_LONG, 0, MPI_COMM_WORLD);

        bool localResult = true;

        for (i = 0; i < 10; i++)
        {
            if (!checkNumber(testedNumber, subBaseTable, 10))
            {
                localResult = false;
            }
        }

        MPI_Barrier(MPI_COMM_WORLD);

        if (processNumber == 0)
        {
            results = (bool *)calloc(numberOfProcesses, sizeof(bool));
            assert(results != NULL);
        }

        MPI_Barrier(MPI_COMM_WORLD);
        MPI_Gather(&localResult, 1, MPI_INT, results, 1, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Barrier(MPI_COMM_WORLD);

        if (processNumber == 0)
        {
            for (i = 0; i < numberOfProcesses; i++)
            {
                if (results[i] == false)
                {
                    isPrime = false;
                }
            }
        }
    }

    if (processNumber == 0)
    {

        if (isPrime)
        {
            EXIT_CODE = 0;
        }
        else
        {
            EXIT_CODE = 1;
        }

        free(results);
        free(baseTable);
    }
    free(subBaseTable);

    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Finalize();
    if (processNumber == 0)
        exit(EXIT_CODE);
}
