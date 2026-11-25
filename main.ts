// Entry for make.fun news-image-20261124: "Sum up 24 November's world
// news in one image" (Node, standard library only, no network).
//
// The picture is entry.png, stored next to this file. It was painted
// entirely with code (see draw.py, Python + PIL primitives) as a
// newspaper front page for Tuesday 24 November 2026: Iran saying a
// fourth oil tanker hit a naval mine and caught fire east of the Strait
// of Hormuz; Trump possibly gaining up to $15m on paper from Nvidia's
// rally after taking credit for Jensen Huang's return as CEO;
// BepiColombo limping into Mercury orbit after a software glitch cut
// its insertion burn short; two killed and 40 hurt in the Russian
// strike on Zaporizhzhia; Israel killing Hamas security chief Naeem Abu
// Nahel in Gaza; Russian jets triggering Seoul's air raid alert; and
// NATO vowing to defend space.
//
// This program does a single deterministic job: it places that exact
// image at $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png by
// default), byte for byte, so every run shows the judge the same
// picture the repository holds. No network, no state, no randomness:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const here = new URL("./entry.png", import.meta.url);
copyFileSync(here, join(outDir, "entry.png"));
