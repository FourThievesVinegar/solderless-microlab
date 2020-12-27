import React, { useState, useEffect } from "react";
import { Button } from "semantic-ui-react";

import { Header } from "./components/Header";
import { apiUrl } from "./utils";

export function Status(props) {
  const { status } = props;
  const [loading, setLoading] = useState(false);

  const selectOption = (option) => {
    if (loading) return;
    setLoading(true);

    fetch(apiUrl + "select/option/" + option)
      .then((response) => response.json())
      .then((data) => console.log(data));
  };

  useEffect(() => {
    setLoading(false);
  }, [status]);

  return (
    <div>
      <Header>Status</Header>

      {status ? (
        <div className="button-list">
          <p>{status.message}</p>

          {status.options.map((x) => (
            <Button key={x} onClick={() => selectOption(x)} loading={loading}>
              {x}
            </Button>
          ))}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}
