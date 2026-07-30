import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.join(__dirname, 'ΠPaw_Enterprise_Demo.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
const js = scripts[scripts.length - 1][1];
try {
  new Function(js);
  console.log('OK (main script, ' + js.split('\n').length + ' lines)');
} catch (e) {
  console.error(e.message);
  process.exit(1);
}
