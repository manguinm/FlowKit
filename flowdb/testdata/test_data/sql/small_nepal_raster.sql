BEGIN;
CREATE TABLE "population"."small_nepal_raster" ("rid" serial PRIMARY KEY,"rast" raster);
SELECT AddRasterConstraints('population','small_nepal_raster','rast',TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,FALSE,TRUE,TRUE,TRUE,TRUE,TRUE);
END;