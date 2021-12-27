# changelog

Every noteable change is logged here.

## v0.11.2

### Fix

* do not handle single char headlines as no headline (76a05bd6a57f)

## v0.11.1

### Fix

* make level pattern less strict (359910954823)

## v0.11.0

### Feature

* reduce decision time (cd3dc96dc61e)
* move headlines from sections (48b616bce68d)
* use cache to reduce processing time (d24719681e45)
* do not detect headlines with to low char rate in title (3610149795e6)

### Fix

* remove not reachable code (a94715e4bb66)

### Documentation

* clarify interface documentation (3dbbbe96cbb5)

## v0.10.3

### Feature

* skip list item as possible headline (862e7c5a3423)
* extend headlines list (b10317267a49)

## v0.10.2

### Fix

* improve negative caption lookup (025362f89f7f)

## v0.10.1

### Fix

* limit text too match long inputs with regex (79daf64f6665)

## v0.10.0

### Feature

* add table caption checker (9918106aa1d7)
* add single character as figure number (14a38495cab3)

## v0.9.0

### Feature

* add code caption detector (a911bf83a0af)
* add valid headline (ac3680609189)
* strip input data (d4151093105f)

## v0.8.0

### Feature

* add method to check against caption line (f22fb87b6bf2)

## v0.7.0

### Feature

* extend headline list (288b048dbba8)

## v0.6.1

### Fix

* strip after replacing (4cfeef80ad68)

## v0.6.0

### Feature

* move method to verify page number (983870231c00)

## v0.5.2

### Fix

* swap arguments (078a50f518b7)

## v0.5.1

## v0.5.0

### Feature

* add method to verify if headline is table of content (eb9379604be2)

## v0.4.3

### Feature

* add appendix level (3cbe0cced5bf)

## v0.4.2

### Feature

* add `Kapitel 1:`-pattern to leveled parser (f9f7b00cd157)

## v0.4.1

### Feature

* extend public API (cd86e62c7bc6)

### Fix

* fix spelling error (80ebe28e1712)

## v0.4.0

### Feature

* add parameter to change max dots in headline (20b48623584c)
* use no headline check to improve headline parser (7df60e50036b)
* add char headline pattern (73b5a8b4766e)
* add level four char pattern (ca835c662363)

## v0.3.3

### Feature

* introduce invalid roman page numbers (1ce04c4679f8)

### Fix

* fix 988f3482e8e8b refactoring (6f760af9e62f)

## v0.3.2

### Feature

* externalize parameter for noheadline check (988f3482e8e8)

## v0.3.1

### Feature

* extend public API (5caebae93d7c)

### Documentation

* Happy New Year! (791406b572f4)

## v0.3.0

### Feature

* move toc and pagenumber code (05e93c17602c)

## v0.2.1

### Fix

* do not ignore long headlines (bf679a291f05)

## v0.2.0

### Feature

* add strict flag to make headline check more strict (0dfd328b1d50)
* extend valid headline list (125e947018a3)

## v0.1.2

### Fix

* parse late to use other checks before (f7a15b08618b)

## v0.1.1

### Feature

* extend noheadline check (6e403bc2364e)

## v0.1.0

### Feature

* add method to decide if token is a headline (d6cc18557a0d)
* add method to determine headline level (73a156cf4a3e)

## v0.0.0 Initial release

