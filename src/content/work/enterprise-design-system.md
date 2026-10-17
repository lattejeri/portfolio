---
title: Building a successful enterprise design system
byline: Enterprise design system at WorkCover Queensland. My experiences implementing a design system to create lean interfaces and increase designer-developer collaboration.
draft: false
blocks:
  - type: text
    body: <h2>Getting started</h2><h3>Build trust and faith in the idea before beginning</h3><p>Setting off to build a design system from scratch is a big investment in time and resources. And rightly so, any stakeholder likely to be involved with it is going to have their fair share of concerns. In order to get approval to begin developing a design system from scratch, my team did the following:</p><ul><li>Portrayed a successful end-state with examples and references to show stakeholders</li><li>Committed to practicing self-discipline, from initial design to final spec and handover</li><li>Committed to being lean, designing new components only when necessary</li><li>Encouraged Development to help set the architecture of the design system based on their chosen technology</li></ul><h3>Identify your own past mistakes</h3><p>The legacy of previous projects had left our team with an inconsistent set of styles and components across our platforms. Over time, new components would be designed and specified when an existing component could have been used. Over time, the continual process of redesigning components had led to us having multiple versions of similar styles, colours and layouts. To move forward, we needed to accept our past mistakes as design professionals, and commit to 'just one' of everything.</p>
  - type: imageWide
    src: /portfolio/media/wcq-ds/inconsistent-styles.svg
    alt: Four different heading styles, four different button styles and four slightly different blues
    caption: The legacy of previous projects had left us with an inconsistent set of type, colour and interface styles
    framed: true
  - type: text
    body: <h3>Admit you're not the expert in the room</h3><p>We may be design subject matter experts, but definitely not technical ones. We communicated early on that we wanted to learn from the experts how they wanted to build into the future.</p>
  - type: text
    body: <h2>Design components</h2><h3>Foundation elements</h3><p>Below are foundation elements from our Atomic design system:</p>
  - type: imageWide
    src: /portfolio/media/wcq-ds/foundation-elements.jpg
    alt: Colour palette of UI and brand colours in four shades each, alongside the type scale from Heading 1 to Caption small
    framed: true
  - type: text
    body: <h3>Design system components</h3><p>Below are some atoms from our Atomic design system:</p>
  - type: imageWide
    src: /portfolio/media/wcq-ds/atoms-inputs-and-messages.jpg
    alt: Checkboxes, toggles, radio list items, star ratings, badges, text inputs, text areas, pagination and message banners in their different states
    framed: true
  - type: imageWide
    src: /portfolio/media/wcq-ds/atoms-buttons-and-lists.jpg
    alt: A dialog, primary and secondary buttons in each size and state, two-line list items, accordion headings, tabs, dropdowns and a progress wizard
    framed: true
  - type: text
    body: <h3>Design system molecules</h3><p>Below are some molecules from our Atomic design system:</p>
  - type: imageWide
    src: /portfolio/media/wcq-ds/molecules.jpg
    alt: Molecules including an overview card, a contact card, a form section, a progress panel, data tables, an injury card and checklists
    framed: true
  - type: text
    body: <h2>Scalable design</h2><h3>Go Atomic, but adapt it to your organisation</h3><p>We started with an Atomic UI structure as a base, but learnt that it didn't match the way Development were going to build. To better align with Development, we removed the 'organism' layer from our Atomic structure.</p>
  - type: imageWide
    src: /portfolio/media/wcq-ds/atomic-layers.svg
    alt: Atoms, molecules and templates, with the organisms layer faded and crossed out
    caption: The Development team didn't see value in the 'Organism' Atomic layer, so we cut it
    framed: true
  - type: text
    body: <h3>Be lean and consistent</h3><p>To eliminate the risk of inconsistency, we designed universal components, where:</p><ul><li>Design tokens were used to specify a style, meaning changes could be made once globally</li><li>All component spacing adhered to a ¼ rem based grid</li><li>Every colour has meaning or function, e.g. green for success, purple for guidance</li><li>Our type styles were restricted to four headings, two captions and two paragraph styles</li><li>All icons have meaning</li><li>Atoms (like buttons) have as few variations as possible</li></ul><h3>Practice discipline</h3><p>As the maturity of a design system progresses, the need to design new components should diminish. After 'climbing the initial hill' of designing components for the first couple of projects, we'd review as a committee if a new component was ever needed. Using and reusing existing components takes priority over the convenience of designing elements just to meet the needs of a specific project.</p>
  - type: imageWide
    src: /portfolio/media/wcq-ds/maturity-curve.svg
    alt: An S-shaped curve of design system maturity over time, annotated from creating new components, to reusing existing ones, to a fully functioning system
    caption: "'Climbing the hill' of design system maturity"
    framed: true
  - type: text
    body: <h3>Ensure visibility of components</h3><p>Both Design and Development need clear visibility over what components exist and how they're built. We use a combination of Figma, Zeroheight and Storybook to keep visibility of each component in the design system.</p>
  - type: imageWide
    src: /portfolio/media/wcq-ds/design-system-tools.svg
    alt: Figma to design components, Zeroheight to document the system, Storybook to document the code
    caption: Each of the tools used to document and build the design system
    framed: true
  - type: text
    body: <h3>Speak the same language as development</h3><p>One of the biggest insights from the process of building a design system is the importance of using the same language as Development. We encouraged Development to lead the naming conventions of components, to ensure they were global and matched the way they were built. In our component library (Figma), we named elements the same name that they were going to be called in code.</p><p>When documenting components, the Colour, Structure and Typography should be documented in table format using the language that Development are going to use to build.</p>
  - type: imageWide
    src: /portfolio/media/wcq-ds/documentation-attributes.svg
    alt: A numbered component, a colour token, a spacing token and a typography mixin
    caption: The Colour, Structure and Typography should be documented in table format using the language that Development are going to use to build
    framed: true
  - type: text
    body: <h3>Examples of documentation</h3><p>Below are some examples of documented Atomic components. For each Atomic component, the following attributes are documented:</p>
  - type: imageWide
    src: /portfolio/media/wcq-ds/documentation-redlines.jpg
    alt: Redlined labels, buttons, radio buttons and a list item showing spacing tokens and minimum widths
    framed: true
  - type: imageInline
    src: /portfolio/media/wcq-ds/documentation-zeroheight.png
    alt: Zeroheight page for a two line list item with avatar, with tables for its components, typography, colour and structure tokens
    framed: true
---
