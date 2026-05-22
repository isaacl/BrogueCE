Brogue used to come with a file `seed-catalog.txt` which listed the contents of seeds 1-1000. CE no longer includes this, but fortunately it's easier to create your own.

If you run `brogue --help` in a terminal, you should see amongst the options:

```
[--csv] --print-seed-catalog [START NUM LEVELS]
                           (optional csv format)
                           prints a catalog of the first LEVELS levels of NUM
                           seeds from seed START (defaults: 1 1000 5)
```

(On Windows, run `brogue-cmd.bat` instead of `brogue` for this.)

So for example, we could quickly view the first 10 floors of seed 2000 by running

    brogue --print-seed-catalog 2000 1 10

To generate the classic catalog to a file:

    brogue --print-seed-catalog 1 1000 5 > seed-catalog.txt

Keep in mind that writing catalogs isn't very fast.

Note: on Windows there is a bug where the script only shows the output after it's finished. [#399](https://github.com/tmewett/BrogueCE/issues/399)