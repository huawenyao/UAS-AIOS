import fs from 'fs';
const html = fs.readFileSync('c:/Users/ranwu/XiaomiCloud/UAS-AIOS/docs/strategic/demo/ΠPaw_Enterprise_Demo.html', 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
const js = scripts[scripts.length - 1][1];
try {
  new Function(js);
  console.log('OK (main script, ' + js.split('\n').length + ' lines)');
} catch (e) {
  console.error(e.message);
  process.exit(1);
}
