void gen() {
  TCanvas *c1 = new TCanvas();
  TLatex *latex = new TLatex();
  latex->SetTextSize(0.28);
  latex->DrawLatexNDC(0.15, 0.37, "No Plots");
  c1->Print("_static/no_plots.png");
}
