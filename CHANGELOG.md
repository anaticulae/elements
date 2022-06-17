# changelog

Every noteable change is logged here.

## v0.21.0

### Feature

* use simple lookup list (d14f6981ce77)
* add simple negative list lookup (0948809e0885)
* extend noheadline pattern (34e768502121)
* extend noheadline pattern (386ca91c33e8)
* extend headlines (d13649fe9943)

### Fix

* do not hash this complex call (ad8a86c6ba8f)

## v0.20.0

### Feature

* use configo cacher (658f2b713d9e)
* extend page number detector (728f63efac84)

## v0.19.0

### Feature

* add method to parse captions (243ca4a16631)

## v0.18.3

### Feature

* extend no headline decider (5ce01cd125fd)

## v0.18.2

### Feature

* extend caption code word (ae70e373269d)

## v0.18.1

### Feature

* increase required equality (23822be7fdf3)

## v0.18.0

### Feature

* extend invalid headline pattern (c199b884a661)
* reduce range of possible chapter (f316922b3d1f)
* move patch determiner from words (1942c584bf98)

### Fix

* limit regex execution time (5e025f8868a9)
* extend no headline pattern (2ec37e6f639c)

## v0.17.3

### Feature

* handle zero numbered ending (cc1961b1c43c)
* extend headlines (ccf3133e0d9c)

## v0.17.2

### Feature

* extend headlines (702bcb45127d)

### Fix

* adjust appendix headline level (7f52f4082a42)

## v0.17.1

### Feature

* extend abbreviation list (0d485ea5b14c)

## v0.17.0

### Feature

* add explicit figure caption (ab76d7505899)
* extend headline table (d74f66ef8ec4)

### Fix

* do not strip `minus` inside potential number (7c13f59d243f)
* skip too long page numbers as potential page number (a7545b9ef6f1)
* skip missing page number (caa06b5de6fe)

## v0.16.3

### Fix

* make regex robust vs timing problems (bb6450d42971)

## v0.16.2

### Feature

* extend public API (141a2b3e4624)

### Documentation

* adjust method documentation (ba1f42997c80)

## v0.16.1

### Feature

* extend noheadline detector (c84653756c72)

## v0.16.0

### Feature

* extend headline list (9ad1c6ea726e)
* extend headline list (a3b512d2ba18)
* extend noheadline detector (58269c2a72d3)
* extend headline list (4a1985d09f68)
* extend list of headlines (f4085fbaef55)
* add `graph` as valid caption (bb995cbd178f)
* add headlines to public API (2e94d639b784)

### Fix

* return none instead of failing (9b4a7640f17f)
* do not treat headline with high number as toc line (464693f67a28)
* do not skip empty level as first one (1e3b5df4c20e)
* improve stepped parser (22a67f5300ac)
* flatten tocs to work on tocs directly (286c03d37fb7)
* enable grouping non iterable items (ff0ca871897f)

### Documentation

* fix modules path (1810213ada88)

## v0.15.0

### Feature

* add method to determine toc style (df3b494da5ff)
* extend headlines lookup (4e1b82f626ce)

## v0.14.0

### Feature

* make toc decider length dependent (2facaf02bbd8)
* add abstract headline (4d7d33ecfc1f)

## v0.13.1

### Feature

* reduce required rate (856ee2839fef)
* make toc check changeable from outside (53f8cc0b7a27)

## v0.13.0

### Feature

* add method to distinguish between numbered and steps toc (ea17f2c3ae09)
* use cache to reduce execution time (b19d98c04a4d)
* add level steps parser (b65de459dd74)

## v0.12.1

## v0.12.0

### Feature

* extend chapter headlines (a6397a40bcc1)
* add option to detect numbers with spaces inside (3e369cf5cc09)
* treat quotes not as headline (224f370f27a0)
* add method to check that line is a quote (5f4592ea0017)
* skip bib line as potential headline (9c8fd09cf8b0)
* add single char check (bbd6002b8360)

### Documentation

* Happy New Year! (a7878fe1d3cb)

## v0.11.3

### Feature

* improve noheadline checker (61d8b04942f8)
* add missing headline (204cc132a78f)

### Fix

* improve single char check (2fc701390282)

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

