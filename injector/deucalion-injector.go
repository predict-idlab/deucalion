package main

import (
	"github.com/predict-idlab/deucalion/injector/webhook"
	"github.com/spf13/cobra"
	"k8s.io/component-base/cli"
	"os"
)

var Version = "development"

func main() {
	rootCmd := &cobra.Command{
		Use:     "deucalion-injector",
		Version: Version,
	}
	rootCmd.AddCommand(webhook.CmdWebhook)
	rootCmd.AddCommand(manual.CmdManual)
	code := cli.Run(rootCmd)
	os.Exit(code)
}
