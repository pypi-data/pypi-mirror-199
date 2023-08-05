/*
 * Copyright (c) 2021 Arm Limited.
 *
 * SPDX-License-Identifier: MIT
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */

#pragma once

#ifdef __aarch64__

namespace {

void a64_transpose_interleave_12_u8u16(uint16_t *out, const uint8_t *in, size_t width, size_t in_stride, size_t height)
{
    size_t out_stride = 12 * height * sizeof(uint16_t);

    __asm__ __volatile__(
      "cmp %x[height], #0x4\n"
      "blt 10f\n"
      "1:"  // Main row loop: Head
      "mov x24, %x[in]\n"
      "mov x23, %x[out]\n"
      "add x22, x24, %x[in_stride]\n"
      "add x21, x22, %x[in_stride]\n"
      "add x20, x21, %x[in_stride]\n"
      "add %x[in], x20, %x[in_stride]\n"
      "sub %x[height], %x[height], #0x4\n"
      "mov x19, %x[width]\n"
      "cmp x19, #0x18\n"
      "blt 3f\n"
      "2:"  // Main row loop: Unroll column loop
      "ldr q16, [x24], #0x10\n"
      "ushll v27.8h, v16.8b, #0x0\n"
      "ldr d17, [x24], #0x8\n"
      "sub x19, x19, #0x18\n"
      "ushll2 v16.8h, v16.16b, #0x0\n"
      "ldr q26, [x22], #0x10\n"
      "cmp x19, #0x18\n"
      "dup v20.2d, v16.d[0]\n"
      "ldr q25, [x21], #0x10\n"
      "dup v24.2d, v16.d[1]\n"
      "ldr q23, [x20], #0x10\n"
      "ushll v16.8h, v17.8b, #0x0\n"
      "ldr d19, [x22], #0x8\n"
      "mov v24.d[1], v16.d[0]\n"
      "dup v22.2d, v16.d[1]\n"
      "ldr d18, [x21], #0x8\n"
      "ushll v16.8h, v26.8b, #0x0\n"
      "ldr d21, [x20], #0x8\n"
      "mov v20.d[1], v16.d[0]\n"
      "str q27, [x23, #0x0]\n"
      "dup v17.2d, v16.d[1]\n"
      "str q20, [x23, #0x10]\n"
      "ushll2 v16.8h, v26.16b, #0x0\n"
      "mov v17.d[1], v16.d[0]\n"
      "str q17, [x23, #0x20]\n"
      "mov v22.d[1], v16.d[1]\n"
      "ushll v20.8h, v19.8b, #0x0\n"
      "ushll v16.8h, v25.8b, #0x0\n"
      "str q16, [x23, #0x30]\n"
      "ushll2 v16.8h, v25.16b, #0x0\n"
      "dup v17.2d, v16.d[0]\n"
      "dup v19.2d, v16.d[1]\n"
      "ushll v16.8h, v18.8b, #0x0\n"
      "mov v19.d[1], v16.d[0]\n"
      "dup v18.2d, v16.d[1]\n"
      "ushll v16.8h, v23.8b, #0x0\n"
      "mov v17.d[1], v16.d[0]\n"
      "str q17, [x23, #0x40]\n"
      "dup v17.2d, v16.d[1]\n"
      "ushll2 v16.8h, v23.16b, #0x0\n"
      "mov v17.d[1], v16.d[0]\n"
      "str q17, [x23, #0x50]\n"
      "add x23, x23, %x[out_stride]\n"
      "mov v18.d[1], v16.d[1]\n"
      "str q24, [x23, #0x0]\n"
      "ushll v16.8h, v21.8b, #0x0\n"
      "str q22, [x23, #0x10]\n"
      "str q20, [x23, #0x20]\n"
      "str q19, [x23, #0x30]\n"
      "str q18, [x23, #0x40]\n"
      "str q16, [x23, #0x50]\n"
      "add x23, x23, %x[out_stride]\n"
      "bge 2b\n"
      "3:"  // Main row loop: Unroll column loop skip
      "cmp x19, #0xc\n"
      "blt 5f\n"
      "4:"  // Main row loop: Column loop
      "ldr d16, [x24], #0x8\n"
      "sub x19, x19, #0xc\n"
      "ldr d21, [x22], #0x8\n"
      "cmp x19, #0xc\n"
      "ldr d20, [x21], #0x8\n"
      "ldr d19, [x20], #0x8\n"
      "ld1 { v16.s }[2], [x24], #0x4\n"
      "ushll v17.8h, v16.8b, #0x0\n"
      "ld1 { v21.s }[2], [x22], #0x4\n"
      "ushll2 v18.8h, v16.16b, #0x0\n"
      "ld1 { v20.s }[2], [x21], #0x4\n"
      "ld1 { v19.s }[2], [x20], #0x4\n"
      "ushll v16.8h, v21.8b, #0x0\n"
      "str q17, [x23, #0x0]\n"
      "ushll2 v17.8h, v21.16b, #0x0\n"
      "mov v18.d[1], v16.d[0]\n"
      "str q18, [x23, #0x10]\n"
      "dup v16.2d, v16.d[1]\n"
      "mov v16.d[1], v17.d[0]\n"
      "str q16, [x23, #0x20]\n"
      "ushll v16.8h, v20.8b, #0x0\n"
      "str q16, [x23, #0x30]\n"
      "ushll2 v17.8h, v20.16b, #0x0\n"
      "ushll v16.8h, v19.8b, #0x0\n"
      "mov v17.d[1], v16.d[0]\n"
      "str q17, [x23, #0x40]\n"
      "dup v17.2d, v16.d[1]\n"
      "ushll2 v16.8h, v19.16b, #0x0\n"
      "mov v17.d[1], v16.d[0]\n"
      "str q17, [x23, #0x50]\n"
      "add x23, x23, %x[out_stride]\n"
      "bge 4b\n"
      "5:"  // Main row loop: Column loop skip
      "cmp x19, #0x4\n"
      "blt 7f\n"
      "6:"  // Main row loop: width 4 loop: loop
      "ldr s16, [x24], #0x4\n"
      "ushll v19.8h, v16.8b, #0x0\n"
      "ldr s16, [x22], #0x4\n"
      "sub x19, x19, #0x4\n"
      "ushll v18.8h, v16.8b, #0x0\n"
      "ldr s16, [x21], #0x4\n"
      "cmp x19, #0x4\n"
      "ushll v17.8h, v16.8b, #0x0\n"
      "ldr s16, [x20], #0x4\n"
      "str d19, [x23, #0x0]\n"
      "ushll v16.8h, v16.8b, #0x0\n"
      "str d18, [x23, #0x18]\n"
      "str d17, [x23, #0x30]\n"
      "str d16, [x23, #0x48]\n"
      "add x23, x23, #0x8\n"
      "bge 6b\n"
      "7:"  // Main row loop: width 4 loop: skip
      "cmp x19, #0x1\n"
      "blt 9f\n"
      "8:"  // Main row loop: width 1 loop: loop
      "ldr b16, [x24], #0x1\n"
      "ushll v19.8h, v16.8b, #0x0\n"
      "ldr b16, [x22], #0x1\n"
      "sub x19, x19, #0x1\n"
      "ushll v18.8h, v16.8b, #0x0\n"
      "ldr b16, [x21], #0x1\n"
      "cmp x19, #0x1\n"
      "ushll v17.8h, v16.8b, #0x0\n"
      "ldr b16, [x20], #0x1\n"
      "str h19, [x23, #0x0]\n"
      "ushll v16.8h, v16.8b, #0x0\n"
      "str h18, [x23, #0x18]\n"
      "str h17, [x23, #0x30]\n"
      "str h16, [x23, #0x48]\n"
      "add x23, x23, #0x2\n"
      "bge 8b\n"
      "9:"  // Main row loop: width 1 loop: skip
      "add %x[out], %x[out], #0x60\n"
      "cmp %x[height], #0x4\n"
      "bge 1b\n"
      "cbz %x[height], 20f\n"
      "10:"  // Main loop skip

      "11:"  // Tail row loop: Head
      "mov x24, %x[in]\n"
      "mov x23, %x[out]\n"
      "add %x[in], x24, %x[in_stride]\n"
      "sub %x[height], %x[height], #0x1\n"
      "mov x19, %x[width]\n"
      "cmp x19, #0x18\n"
      "blt 13f\n"
      "12:"  // Tail row loop: Unroll column loop
      "ldr q17, [x24], #0x10\n"
      "ushll v16.8h, v17.8b, #0x0\n"
      "ldr d18, [x24], #0x8\n"
      "sub x19, x19, #0x18\n"
      "ushll2 v17.8h, v17.16b, #0x0\n"
      "str q16, [x23, #0x0]\n"
      "cmp x19, #0x18\n"
      "dup v16.2d, v17.d[0]\n"
      "str d16, [x23, #0x10]\n"
      "dup v17.2d, v17.d[1]\n"
      "add x23, x23, %x[out_stride]\n"
      "ushll v16.8h, v18.8b, #0x0\n"
      "mov v17.d[1], v16.d[0]\n"
      "str q17, [x23, #0x0]\n"
      "dup v16.2d, v16.d[1]\n"
      "str d16, [x23, #0x10]\n"
      "add x23, x23, %x[out_stride]\n"
      "bge 12b\n"
      "13:"  // Tail row loop: Unroll column loop skip
      "cmp x19, #0xc\n"
      "blt 15f\n"
      "14:"  // Tail row loop: Column loop
      "ldr d17, [x24], #0x8\n"
      "sub x19, x19, #0xc\n"
      "cmp x19, #0xc\n"
      "ld1 { v17.s }[2], [x24], #0x4\n"
      "ushll v16.8h, v17.8b, #0x0\n"
      "str q16, [x23, #0x0]\n"
      "ushll2 v16.8h, v17.16b, #0x0\n"
      "str d16, [x23, #0x10]\n"
      "add x23, x23, %x[out_stride]\n"
      "bge 14b\n"
      "15:"  // Tail row loop: Column loop skip
      "cmp x19, #0x4\n"
      "blt 17f\n"
      "16:"  // Tail row loop: width 4 loop: loop
      "ldr s16, [x24], #0x4\n"
      "ushll v16.8h, v16.8b, #0x0\n"
      "str d16, [x23, #0x0]\n"
      "sub x19, x19, #0x4\n"
      "add x23, x23, #0x8\n"
      "cmp x19, #0x4\n"
      "bge 16b\n"
      "17:"  // Tail row loop: width 4 loop: skip
      "cmp x19, #0x1\n"
      "blt 19f\n"
      "18:"  // Tail row loop: width 1 loop: loop
      "ldr b16, [x24], #0x1\n"
      "ushll v16.8h, v16.8b, #0x0\n"
      "str h16, [x23, #0x0]\n"
      "sub x19, x19, #0x1\n"
      "add x23, x23, #0x2\n"
      "cmp x19, #0x1\n"
      "bge 18b\n"
      "19:"  // Tail row loop: width 1 loop: skip
      "add %x[out], %x[out], #0x18\n"
      "cmp %x[height], #0x1\n"
      "bge 11b\n"
      "20:"  // Done

      : [height] "+&r" (height), [in] "+&r" (in), [out] "+&r" (out)
      : [in_stride] "r" (in_stride), [out_stride] "r" (out_stride), [width] "r" (width)
      : "cc", "memory", "v16", "v17", "v18", "v19", "v20", "v21", "v22", "v23", "v24", "v25", "v26", "v27", "x19", "x20", "x21", "x22", "x23", "x24"
    );
}

} // anonymous namespace
template<>
void Transform<12, 1, true, VLType::None>(
    uint16_t *out, const uint8_t *in, int stride, int x0, int xmax, int k0, int kmax)
{
    a64_transpose_interleave_12_u8u16(
        out,
        in + k0 * stride + x0,
        (xmax-x0),
        stride * sizeof(uint8_t),
        (kmax-k0)
    );
}

#endif
