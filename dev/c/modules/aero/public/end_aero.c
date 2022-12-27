#include <stdlib.h>

#include "../../models/models.h"

void end_aero(int n_te, Aero *aero)
{

    free(aero->source);

    free(aero->doublet);

    free(aero->vel);

    free(aero->cp);

    free(aero->transpiration);

    for (int i = 0; i < n_te; i++)
    {
        free(aero->wake[i].area);
        free(aero->wake[i].circulation);
    }

    free(aero->wake);

    free(aero->vel_matrix_doublet);

    free(aero->vel_array_source);

}