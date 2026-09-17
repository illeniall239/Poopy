# Record memory size

Topic: 1. How computers run code
Difficulty: 2 of 3

## Problem

Memory is a long row of numbered bytes. Languages like C, Rust and Go lay out a record (a struct) as its fields one after another, but a CPU reads a field fastest when the field starts at an address that is a multiple of the field's size. So the compiler inserts unused padding bytes.

Field types and their sizes in bytes:

| type | size |
|------|------|
| `"bool"`, `"i8"` | 1 |
| `"i16"` | 2 |
| `"i32"`, `"f32"` | 4 |
| `"i64"`, `"f64"`, `"ptr"` | 8 |

Write two functions:

- `recordSize(fields)` takes the field types in declaration order and returns the record's size in bytes. Lay the fields out in the given order (never reorder them). Each field starts at the first offset at or after the end of the previous field that is a multiple of the field's size. After the last field, round the total up to a multiple of the largest field size in the record, so records can sit next to each other in an array. A record with no fields has size `0`.
- `arraySize(fields, count)` returns the bytes used by an array of `count` such records stored back to back, with nothing else.

## Examples

```
recordSize(["i8", "i32"])        → 8    i8 at 0, 3 padding bytes, i32 at 4
recordSize(["i32", "i8"])        → 8    i32 at 0, i8 at 4, 3 bytes of padding at the end
recordSize(["i8", "i64", "i8"])  → 24
recordSize(["i64", "i8", "i8"])  → 16
recordSize([])                   → 0
arraySize(["i32", "i8"], 1000)   → 8000
```

## Constraints

- `fields` has 0 to 20 entries, each one of the type names above.
- `0 <= count <= 10000000`.

## Hints

1. Draw 24 boxes for the bytes of `["i8", "i64", "i8"]` and colour in where each field goes. Where did the gaps come from?
2. You are at offset 1 and the next field needs a multiple of 8. How can you compute the next multiple with arithmetic instead of counting up one byte at a time?
3. What do you need to remember while walking the fields, apart from the current offset, to do the final rounding?
4. Why does `["i32", "i8"]` need padding at the end even though nothing comes after the `i8`? Think about where a second record in an array would start.

## Explain-back

- Why can reordering the same fields change the size of a record? Which order wastes the least space?
- Why does an array of records laid out back to back scan faster than an array of references to separately allocated objects?
- What are the time and space complexity of `recordSize` and of `arraySize`? Does `arraySize` need to look at every record?
- In JavaScript, an array of objects holds references. What would `arraySize` measure in that case, and where do the objects themselves live?
