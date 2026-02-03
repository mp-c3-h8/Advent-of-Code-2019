#include <stdio.h>
#include <stdlib.h>

typedef struct
{
    int *items;
    size_t count;
    size_t capacity;
} da;

void da_init(da *a, size_t initialSize)
{
    a->items = malloc(initialSize * sizeof(int));
    if (a->items == NULL)
    {
        printf("Memory not allocated.\n");
        exit(1);
    }
    a->count = 0;
    a->capacity = initialSize;
}

void da_append(da *a, int element)
{
    if (a->count == a->capacity)
    {
        a->capacity *= 2;
        int *temp = realloc(a->items, a->capacity * sizeof(int));
        if (!temp)
        {
            printf("Memory not allocated.\n");
            exit(EXIT_FAILURE);
        }
        a->items = temp;
    }
    a->items[a->count++] = element;
}

void da_free(da *a)
{
    free(a->items);
    a->items = NULL;
    a->count = a->capacity = 0;
}

da parse_data()
{
    da masses;
    da_init(&masses, 70);

    FILE *data = fopen("./input.txt", "r");
    if (data == NULL)
    {
        printf("Not able to open the file.\n");
        exit(EXIT_FAILURE);
    }
    int mass;
    while (fscanf(data, "%d", &mass) == 1)
    {
        da_append(&masses, mass);
    }
    fclose(data);
    return masses;
}

int main()
{
    da masses = parse_data();

    // part 1
    int part1 = 0;
    for (size_t i = 0; i < masses.count; ++i)
    {
        part1 += (masses.items[i] / 3 - 2);
    }
    printf("Part 1: %d \n", part1);

    // part 2
    int part2 = 0;
    int fuel = 0;
    for (size_t i = 0; i < masses.count; ++i)
    {
        fuel = (masses.items[i] / 3 - 2);

        while (fuel > 0)
        {
            part2 += fuel;
            fuel = (fuel / 3 - 2);
        }
    }
    printf("Part 2: %d \n", part2);

    da_free(&masses);

    return 0;
}