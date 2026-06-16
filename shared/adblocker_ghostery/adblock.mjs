/**
 * Reads from stdin composite keys in format:
 *   <url>\x00<sourceUrl>\x00<type>
 *
 * For each stdin line prints the same composite key if it is blocked by adblocker:
 *   <url>\x00<sourceUrl>\x00<type>
 *
 *   node adblock_check.mjs
 */

import { FiltersEngine, Request } from "@ghostery/adblocker";
import * as readline from "readline";

const DELIM = "\x00";

async function main() {
    let engine;
    try {
        engine = await FiltersEngine.fromLists(fetch, [
            "https://easylist.to/easylist/easylist.txt",
            "https://easylist.to/easylist/easyprivacy.txt",
        ]);
    } catch (err) {
        process.stderr.write(`[adblock_check] Engine load error: ${err}\n`);
        process.exit(1);
    }

    const rl = readline.createInterface({
        input: process.stdin,
        crlfDelay: Infinity,
    });

    for await (const line of rl) {
        const trimmed = line.trim();
        if (!trimmed) continue;

        const parts = trimmed.split(DELIM);
        if (parts.length !== 3) continue;

        const [url, sourceUrl, type] = parts;
        if (!url || !url.startsWith("http")) continue;

        try {
            const req = Request.fromRawDetails({ url, sourceUrl, type });
            const { match } = engine.match(req);
            if (match) {
                process.stdout.write(trimmed + "\n");
            }
        } catch {
        }
    }
}

main();
