document.addEventListener("DOMContentLoaded", function (event) {
  // Masking the inputs
  $(".amount-redeemed")
    .maskMoney({
      prefix: "R$ ",
      decimal: ",",
      thousands: ".",
      allowNegative: false,
    })
    .maskMoney("mask");

  $(".overview-input")
    .maskMoney({
      prefix: "R$ ",
      decimal: ",",
      thousands: ".",
      allowNegative: true,
    })
    .maskMoney("mask");

  $("input.amount-redeemed").prop("readonly", true);
  $("input.overview-input").prop("readonly", true);

  fillAnalytics();
});

// Function to fill the graphics
function fillAnalytics() {
  const analyticsSection = document.getElementById("analytics-section");
  const gainAnalyCol = document.getElementById("gain-analy");
  const expAnalyCol = document.getElementById("exp-analy");

  const ctxExpenses = document.getElementById("graphic-expenses");
  const expenses_string = document.getElementById("expenses_list");

  const ctxGains = document.getElementById("graphic-gains");
  const gains_string = document.getElementById("gains_list");

  if (expenses_string == null) {
    if (gains_string == null) {
      analyticsSection.classList.add("d-none");
    }

    expAnalyCol.classList.add("d-none");
  } else {
    if (gains_string == null) {
      expAnalyCol.classList.remove("col-md-6");
      expAnalyCol.classList.add("col-md-12");
    }

    const expenses_string_val = expenses_string.value;
    const expenses_replace = expenses_string_val.replace(/'/g, '"');
    const expenses_list = JSON.parse(expenses_replace);
    const sorted_expenses = Object.entries(expenses_list)
      .filter(([_, value]) => value > 0)
      .sort((a, b) => b[1] - a[1]);
    const expenses_labels = sorted_expenses.map(([label]) => label);
    const data_chart_expenses = sorted_expenses.map(([_, value]) => value);

    const color_map_expenses = {
      tax: "#eb3636ff",
      food: "#4bc0c0",
      transport: "#8056ffff",
      leisure: "#ff66adff",
      shopping: "#eb7324ff",
      studies: "#51e014ff",
      health: "#e2187aff",
      transfer: "#badd1eff",
      emergency: "#206e19ff",
      other: "#c6cbd4ff",
    };

    const expenses_colors = sorted_expenses.map(
      ([label]) => color_map_expenses[label]
    );

    const configExpenses = {
      type: "doughnut",
      data: {
        labels: expenses_labels,
        datasets: [
          {
            label: "Count of Expenses",
            data: data_chart_expenses,
            backgroundColor: expenses_colors,
          },
        ],
      },
      options: {
        maintainAspectRatio: true,
        plugins: {
          legend: {
            position: "right",
            align: "center",
            labels: {
              generateLabels(chart) {
                const total = data_chart_expenses.reduce((a, b) => a + b, 0);

                const data = chart.data;
                return data.labels.map((label, i) => {
                  const value = data.datasets[0].data[i];
                  const percentage = (value / total) * 100;

                  return {
                    text: `${label} (${percentage.toFixed(0)}%)`,
                    fillStyle: data.datasets[0].backgroundColor[i],
                    index: i,
                  };
                });
              },
            },
          },
        },
      },
    };

    new Chart(ctxExpenses, configExpenses);
  }

  if (gains_string == null) {
    gainAnalyCol.classList.add("d-none");
  } else {
    if (expAnalyCol.classList.contains("d-none")) {
      gainAnalyCol.classList.remove("col-md-6");
      gainAnalyCol.classList.add("col-md-12");
    }

    let gains_string_val = gains_string.value;
    const gains_replace = gains_string_val.replace(/'/g, '"');

    const gains_list = JSON.parse(gains_replace);
    const sorted_gains = Object.entries(gains_list)
      .filter(([_, value]) => value > 0)
      .sort((a, b) => b[1] - a[1]);
    const gains_labels = sorted_gains.map(([label]) => label);
    const data_chart_gains = sorted_gains.map(([_, value]) => value);

    const color_map_gains = {
      salary: "#36a2eb",
      extra_income: "#4bc0c0",
      capital_gain: "#ffcd56",
      transfer: "#9966ff",
      other: "#c9cbcf",
    };

    const gains_colors = sorted_gains.map(([label]) => color_map_gains[label]);

    const configGains = {
      type: "doughnut",
      data: {
        labels: gains_labels,
        datasets: [
          {
            label: "Count of Gains",
            data: data_chart_gains,
            backgroundColor: gains_colors,
          },
        ],
      },
      options: {
        maintainAspectRatio: true,
        plugins: {
          legend: {
            position: "right",
            align: "center",
            labels: {
              generateLabels(chart) {
                const total = data_chart_gains.reduce((a, b) => a + b, 0);

                const data = chart.data;
                return data.labels.map((label, i) => {
                  const value = data.datasets[0].data[i];
                  const percentage = (value / total) * 100;

                  return {
                    text: `${label} (${percentage.toFixed(0)}%)`,
                    fillStyle: data.datasets[0].backgroundColor[i],
                    index: i,
                  };
                });
              },
            },
          },
        },
      },
    };

    new Chart(ctxGains, configGains);
  }
}

// Function to fill the modal content based on transaction type
function contentToRow(selectValue) {
  console.log("contentToRowCalled");
  const emptyRow = document.getElementById("section_by_type");
  const modalHeader = document.getElementById("modal-header");
  const modalFooter = document.getElementById("modal-footer");

  if (selectValue == "gain") {
    emptyRow.innerHTML = "";
    let row = document.createElement("div");

    row.innerHTML = `
    <div class="row">
        <div class="col-md-12">
        <label for="category-select">Category:</label>
        <select
            class="form-select"
            name="category-select"
            id="category-select"
            required
        >
            <option value="" selected disabled>
            Click here to select
            </option>
            <option value="salary">Salary</option>
            <option value="extra_income">Extra Income</option>
            <option value="capital_gain"> Capital Gain (Investments gains)</option>
            <option value="transfer">Transfer</option>
            <option value="other">Other gain</option>
        </select>
        </div>
    </div>

    <div class="row mt-3">
        <div class="col-md-12">
        <label for="transaction-date">Transaction date:</label>
        <input
            type="date"
            class="form-control"
            name="transaction-date"
            id="transaction-date"
            required
        />
        </div>
    </div>

    <div class="row mt-3">
        <div class="col-md-12">
        <label for="amount">Amount (R$):</label>
        <input
            type="text"
            class="form-control"
            name="amount"
            id="amount"
            placeholder="Ex: 200,00"
            required
        />
        </div>
    </div>

    <div class="row mt-3">
        <div class="col-md-12">
        <label for="payment-receipt">Payment receipt (Optional):</label>
        <input
            type="file"
            class="form-control"
            name="payment-receipt"
            id="payment-receipt"
        />
        </div>
    </div>

    <div class="row mt-3">
        <div class="col-md-12">
        <label for="description">Description:</label>
        <textarea
            class="form-control"
            name="description"
            id="description"
            placeholder="Ex: Transfer by son..."
        ></textarea>
        </div>
    </div>`;

    emptyRow.appendChild(row);
    if (emptyRow.classList.contains("d-none")) {
      emptyRow.classList.remove("d-none");
    }

    modalHeader.classList.add("gain");
    if (modalHeader.classList.contains("expense")) {
      modalHeader.classList.remove("expense");
    }

    modalFooter.classList.add("gain");
    if (modalFooter.classList.contains("expense")) {
      modalFooter.classList.remove("expense");
    }
  } else {
    emptyRow.innerHTML = "";
    let row = document.createElement("div");

    row.innerHTML = `
    <div class="row">
        <div class="col-md-12">
        <label for="category-select">Category:</label>
        <select
            class="form-select"
            name="category-select"
            id="category-select"
            required
        >
            <option value="" selected disabled>
            Click here to select
            </option>
            <option value="tax">Tax</option>
            <option value="food">Food</option>
            <option value="transport">Transport</option>
            <option value="leisure">Leisure/family</option>
            <option value="shopping">Shopping (clothing, eletronics, etc)</option>
            <option value="studies">Studies</option>
            <option value="health">doctor/Health</option>
            <option value="transfer">Transfer</option>
            <option value="emergency">Emergency</option>
            <option value="other">Other expense</option>
        </select>
        </div>
    </div>

    <div class="row mt-3">
        <div class="col-md-12">
            <label for="fixed-cost-select">Fixed cost?:</label>
            <select
                class="form-select"
                name="fixed-cost-select"
                id="fixed-cost-select"
                required
            >
                <option value="" selected disabled>
                Click here to select
                </option>
                <option value="yes">Yes</option>
                <option value="no">No</option>
            </select>
        </div>
    </div>

    <div class="row mt-3">
        <div class="col-md-12">
        <label for="transaction-date">Transaction date:</label>
        <input
            type="date"
            class="form-control"
            name="transaction-date"
            id="transaction-date"
            required
        />
        </div>
    </div>

    <div class="row mt-3">
        <div class="col-md-12">
        <label for="amount">Amount (R$):</label>
        <input
            type="text"
            class="form-control"
            name="amount"
            id="amount"
            placeholder="Ex: 91,00"
            required
        />
        </div>
    </div>

    <div class="row mt-3">
        <div class="col-md-12">
        <label for="payment-receipt">Payment receipt (Optional):</label>
        <input
            type="file"
            class="form-control"
            name="payment-receipt"
            id="payment-receipt"
        />
        </div>
    </div>

    <div class="row mt-3">
        <div class="col-md-12">
        <label for="description">Description:</label>
        <textarea
            class="form-control"
            name="description"
            id="description"
            placeholder="Ex: Watter tax payment..."
        ></textarea>
        </div>
    </div>`;

    emptyRow.appendChild(row);

    if (emptyRow.classList.contains("d-none")) {
      emptyRow.classList.remove("d-none");
    }

    modalHeader.classList.add("expense");
    if (modalHeader.classList.contains("gain")) {
      modalHeader.classList.remove("gain");
    }

    modalFooter.classList.add("expense");
    if (modalFooter.classList.contains("gain")) {
      modalFooter.classList.remove("gain");
    }
  }

  // Masking amount input for the both
  $("#amount").maskMoney({
    decimal: ",",
    thousands: ".",
    allowNegative: false,
  });
}

// Function to delete transactions
function deleteTransaction(button) {
  const buttonId = button.id;
  const transactionId = buttonId.split("-")[1];

  if (window.confirm("Are you sure to delete this transaction?")) {
    fetch("/transactions", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ transaction_id: transactionId }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP Error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        window.location.href = "/transactions";
      })
      .catch((error) => {
        console.error("Something got wrong:", error);
      });
  } else {
    console.log("TUNE NADA!!");
  }
}
