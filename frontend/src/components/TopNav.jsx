const TopNav = () => {
  return (
    <header style={styles.nav}>
      <div style={styles.brand}>🇰🇪 Kenya Toll Collection</div>

      <nav style={styles.links}>
        <span style={{ ...styles.link, ...styles.active }}>Home</span>
        <span style={styles.link}>About</span>
        <span style={styles.link}>Contact</span>
      </nav>
    </header>
  );
};

export default TopNav;

/* ================= STYLES ================= */

const styles = {
  nav: {
    height: "56px",
    width: "100%",
    background: "#ffffff",
    borderBottom: "1px solid #E5E7EB",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 24px",
    position: "relative",
    zIndex: 20
  },
  brand: {
    fontWeight: 700,
    fontSize: "15px"
  },
  links: {
    display: "flex",
    gap: "20px",
    fontSize: "14px"
  },
  link: {
    color: "#6B7280"
  },
  active: {
    color: "#2563EB",
    fontWeight: 600
  }
};
