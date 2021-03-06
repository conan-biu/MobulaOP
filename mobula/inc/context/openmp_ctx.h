#ifndef MOBULA_INC_CONTEXT_OPENMP_CTX_H_
#define MOBULA_INC_CONTEXT_OPENMP_CTX_H_

#include <omp.h>

namespace mobula {

#define KERNEL_RUN(a) (a)
#ifndef _MSC_VER
#define __pragma(id) _Pragma(#id)
#endif

MOBULA_DEVICE inline int get_num_threads() { return omp_get_num_threads(); }

MOBULA_DEVICE inline int get_thread_num() { return omp_get_thread_num(); }

template <typename Func>
MOBULA_DEVICE void parfor(const size_t n, Func F) {
  INDEX_TYPE_SWITCH(n, {
    __pragma(omp parallel for) for (index_t i = 0; i < static_cast<index_t>(n);
                                     ++i) {
      F(i);
    }
  });
}

inline void __syncthreads() {
#pragma omp barrier
}

}  // namespace mobula

#endif  // MOBULA_INC_CONTEXT_OPENMP_CTX_H_
