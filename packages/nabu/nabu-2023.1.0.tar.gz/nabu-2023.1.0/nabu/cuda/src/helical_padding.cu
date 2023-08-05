
// see  nabu/pipeline/helical/filtering.py for details

__global__ void padding(
    float* data,
    int* mirror_indexes,
    
#if defined(MIRROR_CONSTANT_VARIABLE_ROT_POS) || defined(MIRROR_EDGES_VARIABLE_ROT_POS)
    int *rot_axis_pos,
#else
    int rot_axis_pos,    
#endif
    int Nx,
    int Ny,
    int Nx_padded,
    int pad_left_len,
    int pad_right_len
#if defined(MIRROR_CONSTANT) || defined(MIRROR_CONSTANT_VARIABLE_ROT_POS)
    ,float pad_left_val,
    float pad_right_val    
#endif
) {
  
  int x = blockDim.x * blockIdx.x + threadIdx.x;
  int y = blockDim.y * blockIdx.y + threadIdx.y;
    
  if ((x >= Nx_padded) || (y >= Ny) || x < Nx) return;
    
  int idx = y*Nx_padded  +  x;

  int y_mirror = mirror_indexes[y];
  
  int x_mirror =0 ; 
 
#if defined(MIRROR_CONSTANT_VARIABLE_ROT_POS) || defined(MIRROR_EDGES_VARIABLE_ROT_POS)
  int two_rots = rot_axis_pos[y] + rot_axis_pos[y_mirror];
#else
  int two_rots = 2*rot_axis_pos ;
#endif

  if( two_rots > Nx)  {
    x_mirror = two_rots - x ;
    if (x_mirror  < 0 ) {
#if defined(MIRROR_CONSTANT) || defined(MIRROR_CONSTANT_VARIABLE_ROT_POS)
      if( x < Nx_padded - pad_left_len) {
	data[idx] = pad_left_val;
      } else {
	data[idx] = pad_right_val; 
      }
#else
      if( x < Nx_padded - pad_left_len) {
	data[idx] = data[y_mirror*Nx_padded  + 0];
      } else {
	data[idx] = data[y*Nx_padded  +  0];
      }
#endif

    } else {
      data[idx] = data[y_mirror*Nx_padded  +  x_mirror];
    }
  } else {
    x_mirror = two_rots - (x - Nx_padded) ;
    if (x_mirror  > Nx-1 ) {
#if defined(MIRROR_CONSTANT) || defined(MIRROR_CONSTANT_VARIABLE_ROT_POS)
      if( x < Nx_padded - pad_left_len) {
	data[idx] =  pad_left_val ;
      } else {
	data[idx] = pad_right_val;
      }
#else
      if( x < Nx_padded - pad_left_len) {
	data[idx] = data[y*Nx_padded  + Nx - 1 ];
      } else {
	data[idx] = data[y_mirror*Nx_padded  +  Nx-1];
      }
#endif

    } else {
      data[idx] = data[y_mirror*Nx_padded  +  x_mirror];
    }
  }
  return;
}

