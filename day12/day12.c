#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct
{
    size_t sz;
    size_t cap;
    int64_t *v;
} vec_t;

vec_t *
vec_new()
{
    vec_t *v = malloc(sizeof(vec_t));
    v->cap = 1024;
    v->v = malloc(v->cap * sizeof(int64_t));
    v->sz = 0;
    return v;
}

vec_t *
vec_cpy(vec_t *v)
{
    if (!v)
        return NULL;
    vec_t *cpy = malloc(sizeof(vec_t));
    cpy->sz = v->sz;
    cpy->cap = v->sz;
    cpy->v = malloc(cpy->cap * sizeof(int64_t));
    for (size_t i = 0; i < cpy->sz; i++)
    {
        cpy->v[i] = v->v[i];
    }
    return cpy;
}

void vec_reset(vec_t *v)
{
    v->sz = 0;
}

size_t
vec_size(vec_t *v)
{
    return v->sz;
}

int64_t
vec_get(vec_t *v, size_t n)
{
    return v->v[n];
}

void vec_set(vec_t *v, size_t n, int64_t d)
{
    if (n + 1 > v->cap)
    {
        v->cap *= 2;
        v->cap = v->cap > n + 1 ? v->cap : n + 1;
        v->v = realloc(v->v, v->cap * sizeof(int64_t));
    }
    v->v[n] = d;
    v->sz = v->sz > n + 1 ? v->sz : n + 1;
}

void vec_append(vec_t *v, int64_t d)
{
    if (v->sz == v->cap)
    {
        v->cap *= 2;
        if (v->cap == 0)
            v->cap = 1024;
        v->v = realloc(v->v, v->cap * sizeof(int64_t));
    }
    v->v[v->sz++] = d;
}

void vec_free(vec_t *v)
{
    if (!v)
        return;
    free(v->v);
    free(v);
}

void axis(vec_t *coord, vec_t *vel, size_t i, size_t j)
{
    if (vec_get(coord, i) < vec_get(coord, j))
    {
        vec_set(vel, i, vec_get(vel, i) + 1);
    }
    else if (vec_get(coord, i) > vec_get(coord, j))
    {
        vec_set(vel, i, vec_get(vel, i) - 1);
    }
}

int64_t gcd(int64_t a, int64_t b)
{
    if (a == 0)
        return b;
    return gcd(b % a, a);
}

int64_t lcm(int64_t a, int64_t b)
{
    return (a / gcd(a, b)) * b;
}

void solve(int _)
{
    vec_t *x, *y, *z;
    vec_t *ix, *iy, *iz;
    vec_t *vx, *vy, *vz;
    int a, b, c;
    size_t n = 0;
    x = vec_new();
    y = vec_new();
    z = vec_new();
    ix = vec_new();
    iy = vec_new();
    iz = vec_new();
    vx = vec_new();
    vy = vec_new();
    vz = vec_new();

    FILE *data = fopen("./input.txt", "r");
    if (data == NULL)
    {
        printf("Not able to open the file.\n");
        exit(EXIT_FAILURE);
    }

    while (fscanf(data, "<x=%d, y=%d, z=%d>\n", &a, &b, &c) != EOF)
    {
        vec_append(x, a);
        vec_append(y, b);
        vec_append(z, c);
        vec_append(ix, a);
        vec_append(iy, b);
        vec_append(iz, c);
        vec_append(vx, 0);
        vec_append(vy, 0);
        vec_append(vz, 0);
        n++;
    }

    if (!_)
    {
        size_t t;
        int64_t e = 0;

        for (t = 0; t < 1000; t++)
        {
            for (size_t i = 0; i < n; i++)
            {
                for (size_t j = 0; j < n; j++)
                {
                    axis(x, vx, i, j);
                    axis(y, vy, i, j);
                    axis(z, vz, i, j);
                }
            }
            for (size_t i = 0; i < n; i++)
            {
                vec_set(x, i, vec_get(x, i) + vec_get(vx, i));
                vec_set(y, i, vec_get(y, i) + vec_get(vy, i));
                vec_set(z, i, vec_get(z, i) + vec_get(vz, i));
            }
        }

        for (size_t i = 0; i < n; i++)
        {
            int64_t k = 0, p = 0;
            p += labs(vec_get(x, i));
            p += labs(vec_get(y, i));
            p += labs(vec_get(z, i));
            k += labs(vec_get(vx, i));
            k += labs(vec_get(vy, i));
            k += labs(vec_get(vz, i));
            e += k * p;
        }

        printf("%" PRId64 "\n", e);
    }
    else
    {
        int64_t px = 0, py = 0, pz = 0;
        while (1)
        {
            int yes = 1;
            for (size_t i = 0; i < n; i++)
            {
                for (size_t j = 0; j < n; j++)
                {
                    axis(x, vx, i, j);
                }
            }
            for (size_t i = 0; i < n; i++)
            {
                vec_set(x, i, vec_get(x, i) + vec_get(vx, i));
                if (vec_get(x, i) != vec_get(ix, i))
                    yes = 0;
                if (vec_get(vx, i) != 0)
                    yes = 0;
            }
            px++;
            if (yes)
                break;
        }
        while (1)
        {
            int yes = 1;
            for (size_t i = 0; i < n; i++)
            {
                for (size_t j = 0; j < n; j++)
                {
                    axis(y, vy, i, j);
                }
            }
            for (size_t i = 0; i < n; i++)
            {
                vec_set(y, i, vec_get(y, i) + vec_get(vy, i));
                if (vec_get(y, i) != vec_get(iy, i))
                    yes = 0;
                if (vec_get(vy, i) != 0)
                    yes = 0;
            }
            py++;
            if (yes)
                break;
        }
        while (1)
        {
            int yes = 1;
            for (size_t i = 0; i < n; i++)
            {
                for (size_t j = 0; j < n; j++)
                {
                    axis(z, vz, i, j);
                }
            }
            for (size_t i = 0; i < n; i++)
            {
                vec_set(z, i, vec_get(z, i) + vec_get(vz, i));
                if (vec_get(z, i) != vec_get(iz, i))
                    yes = 0;
                if (vec_get(vz, i) != 0)
                    yes = 0;
            }
            pz++;
            if (yes)
                break;
        }
        printf("%" PRId64 "\n", lcm(px, lcm(py, pz)));
    }

    vec_free(vz);
    vec_free(vy);
    vec_free(vx);
    vec_free(iz);
    vec_free(iy);
    vec_free(ix);
    vec_free(z);
    vec_free(y);
    vec_free(x);
}

int main()
{
    solve(0);
    solve(1);
    return 0;
}