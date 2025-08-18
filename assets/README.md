# Assets Directory

This directory contains static assets for the Stockie Streamlit application.

## Structure

```
assets/
├── css/
│   └── custom.css          # Custom CSS styles
├── images/
│   └── (image files)       # Logo, icons, charts, etc.
└── README.md              # This file
```

## Usage

### CSS Files
- `custom.css`: Main stylesheet for the application
- Import in Streamlit using: `st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)`

### Images
- Store logos, icons, background images, etc.
- Reference in Streamlit using: `st.image("assets/images/filename.png")`

### Adding New Assets

1. **Images**: Place in `assets/images/`
   - Supported formats: PNG, JPG, JPEG, GIF, SVG
   - Recommended: Use PNG for logos/icons, JPG for photos

2. **CSS**: Add styles to `assets/css/custom.css`
   - Use CSS variables for consistent theming
   - Follow existing naming conventions

3. **Other Files**: Create subdirectories as needed
   - `assets/fonts/` for custom fonts
   - `assets/data/` for sample data files
   - `assets/icons/` for icon sets

## Best Practices

- Keep file sizes small for faster loading
- Use descriptive filenames
- Optimize images before adding
- Document any new asset types

