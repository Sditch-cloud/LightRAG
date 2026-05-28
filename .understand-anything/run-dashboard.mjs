// Wrapper to start vite with GRAPH_DIR set
process.env.GRAPH_DIR = 'E:\\temp-workspace\\LightRAG';
process.chdir('C:\\Users\\UASD-SHIYIFU\\.copilot\\installed-plugins\\_direct\\Lum1104--Understand-Anything--understand-anything-plugin\\packages\\dashboard');

// Import and run vite cli using file:// URL
const vitePath = new URL('file:///C:/Users/UASD-SHIYIFU/.copilot/installed-plugins/_direct/Lum1104--Understand-Anything--understand-anything-plugin/packages/dashboard/node_modules/vite/bin/vite.js');
import(vitePath);
