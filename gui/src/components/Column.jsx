import * as React from "react";
import "../styles/column.css";

const Column = ({ span, children }) => (
  <div className={`column column-span-${span}`}>{children}</div>
);

export default Column;
