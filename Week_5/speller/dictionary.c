// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "dictionary.h"
#include "string.h"

const unsigned int N = 27;
// Represents a node in a hash table
typedef struct node
{
    bool gotit;
    struct node *next[N];
}
node;

// TODO: Choose number of buckets in hash table

// Hash table
node *table;

bool got_the_string(node *X, const char *s, int n)
{
    //last chat in word
    if (s[n] == '\0')
    {
        return X->gotit;
    }

    int re = tolower(s[n]) - 96;
    if (re <= 0)
    {
        re = 0;
    }

    //Null hash table
    if (X->next[re] == NULL)
    {
        return 0;
    }

    return got_the_string(X->next[re], s, n + 1);
}

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    return got_the_string(table, word, 0);
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false


//set node to not found and make all next to NULL
void intlizeNode(node *X)
{
    X->gotit = 0;
    for (int i = 0; i < N; i++)
    {
        X->next[i] = NULL;
    }
}

unsigned int size_of_dic = 0;

bool AddToHash(node *X, char *s, int n)
{
    //got to last char;
    if (s[n] == '\0')
    {
        size_of_dic += !X->gotit;
        X->gotit = 1;
        return 1;
    }

    //index of the char in hash table
    int re = tolower(s[n]) - 96;
    if (re <= 0)
    {
        re = 0;
    }

    if (X->next[re] == NULL)
    {
        node *tmp = malloc(sizeof(node));
        //if memory is full
        if (tmp == NULL)
        {
            return 0;
        }
        intlizeNode(tmp);
        X->next[re] = tmp;
    }

    return AddToHash(X->next[re], s, n + 1);
}

bool load(const char *dictionary)
{
    //open the file
    FILE *fn = fopen(dictionary, "rb");
    if (fn == NULL)
    {
        printf("coudn't open file :(\n");
        return 0;
    }

    //creat my table
    table = malloc(sizeof(node));
    intlizeNode(table);

    //read the input from file
    char s[LENGTH + 1];
    while (fscanf(fn, "%s", s) != EOF)
    {
        //add string to table
        if (!AddToHash(table, s, 0))
        {
            unload();
            return 0;
        }
    }

    fclose(fn);
    return 1;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return size_of_dic;
}

void freeNode(node *X)
{
    for (int i = 0; i < N; i++)
    {
        if (X->next[i] != NULL)
        {
            freeNode(X->next[i]);
        }
    }
    free(X);
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    freeNode(table);

    return 1;
}
