const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

// Set the view engine to EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Serve static files (CSS, JS, images) from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// --- Placeholder Data ---
const placeholderData = {
    mods: [
        { name: "Sodium", description: "A performance-focused rendering engine.", image: "https://placehold.co/300x200/555555/EEEEEE?text=Sodium" },
        { name: "Iris Shaders", description: "A modern shaders mod for Minecraft.", image: "https://placehold.co/300x200/555555/EEEEEE?text=Iris" },
        { name: "Fabric API", description: "The core library for most Fabric mods.", image: "https://placehold.co/300x200/555555/EEEEEE?text=Fabric+API" },
        { name: "Just Enough Items (JEI)", description: "View items and recipes.", image: "https://placehold.co/300x200/555555/EEEEEE?text=JEI" }
    ],
    shaders: [
        { name: "BSL Shaders", description: "A cinematic and aesthetic shader pack.", image: "https://placehold.co/300x200/4a4a4a/EEEEEE?text=BSL" },
        { name: "Sildur's Vibrant Shaders", description: "Adds stunning lighting and water effects.", image: "https://placehold.co/300x200/4a4a4a/EEEEEE?text=Sildur's" },
        { name: "Complementary Shaders", description: "Aims to be the best-looking shader pack.", image: "https://placehold.co/300x200/4a4a4a/EEEEEE?text=Complementary" }
    ],
    resourcepacks: [
        { name: "Faithful 32x", description: "A classic pack that doubles the resolution.", image: "https://placehold.co/300x200/6b6b6b/EEEEEE?text=Faithful" },
        { name: "Sphax PureBDCraft", description: "A comic book-style resource pack.", image: "https://placehold.co/300x200/6b6b6b/EEEEEE?text=Sphax" }
    ],
    plugins: [
        { name: "WorldEdit", description: "An in-game map editor for Minecraft.", image: "https://placehold.co/300x200/7c7c7c/EEEEEE?text=WorldEdit" },
        { name: "EssentialsX", description: "The essential suite of commands for servers.", image: "https://placehold.co/300x200/7c7c7c/EEEEEE?text=EssentialsX" }
    ]
};


// --- Routes ---
app.get('/', (req, res) => {
    res.render('pages/index', { title: 'Home' });
});

app.get('/mods', (req, res) => {
    res.render('pages/category', { title: 'Mods', items: placeholderData.mods, category: 'Mods' });
});

app.get('/shaders', (req, res) => {
    res.render('pages/category', { title: 'Shaders', items: placeholderData.shaders, category: 'Shaders' });
});

app.get('/resourcepacks', (req, res) => {
    res.render('pages/category', { title: 'Resource Packs', items: placeholderData.resourcepacks, category: 'Resource Packs' });
});

app.get('/plugins', (req, res) => {
    res.render('pages/category', { title: 'Plugins', items: placeholderData.plugins, category: 'Plugins' });
});


// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
