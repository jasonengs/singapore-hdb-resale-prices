var dagcompnentfuncs = (window.dashAgGridComponentFunctions =
  window.dashAgGridComponentFunctions || {});

dagcompnentfuncs.flatTypeBadge = function (props) {
  const colors = {
    flat_type: {
      "1 Room": { color: { base: "#00A6F4", tint: "#ace5ff" } },
      "2 Room": { color: { base: "#FD9A00", tint: "#ffd4a6" } },
      "3 Room": { color: { base: "#00C951", tint: "#b0f7cb" } },
      "4 Room": { color: { base: "#FB2C36", tint: "#ffc7c7" } },
      "5 Room": { color: { base: "#AD46FF", tint: "#e9d1ff" } },
      Executive: { color: { base: "#d4522a", tint: "#ffcbbc" } },
      "Multi-Generation": {
        color: { base: "#F6339A", tint: "#fec9e6" },
      },
    },
  };

  const color = colors["flat_type"][props.value]["color"];
  return React.createElement(
    "span",
    {
      style: {
        background: color["tint"],
        color: color["base"],
        border: `1px solid ${color["base"]}`,
        borderRadius: "5px",
        padding: "1.5px 8px",
        fontSize: "12px",
        fontWeight: 400,
        letterSpacing: "0.05em",
        whiteSpace: "nowrap",
      },
    },
    props.value,
  );
};
