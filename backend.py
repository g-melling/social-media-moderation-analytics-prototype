import os
import json
import sqlite3
import datetime
from pathlib import Path

import pandas as pd
from matplotlib.figure import Figure


class Backend:
    def __init__(self):
        self.data = {}
        self.audit_log = []
        self._try_restore_on_startup()

    def _require_data(self, *required_tables):
        if not self.data:
            raise ValueError("Load data first.")

        missing = [name for name in required_tables if name not in self.data]
        if missing:
            raise ValueError(f"Missing required data: {', '.join(missing)}. Load data first.")

    def _try_restore_on_startup(self):
        if os.path.exists("backup.json"):
            try:
                with open("backup.json", "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                self.data = {name: pd.DataFrame(records) for name, records in json_data.items()}
                self.log_action("Restored data automatically from backup.json")
            except Exception:
                self.data = {}

    def log_action(self, action):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{timestamp} - {action}"
        self.audit_log.append(entry)

        with open("audit_log.txt", "a", encoding="utf-8") as f:
            f.write(entry + "\n")

    def load_data(self, file_paths=None):
        default_paths = {
            "users": "USERS.csv",
            "posts": "POSTS.csv",
            "interactions": "INTERACTIONS.csv",
            "topics": "TOPICS.csv",
        }
        paths = file_paths or default_paths

        for name in default_paths:
            if name not in paths or not paths[name]:
                raise ValueError(f"No file selected for {name}.")
            if not Path(paths[name]).exists():
                raise FileNotFoundError(f"File not found for {name}: {paths[name]}")

        self.data["users"] = pd.read_csv(paths["users"])
        self.data["posts"] = pd.read_csv(paths["posts"], encoding="latin1")
        self.data["interactions"] = pd.read_csv(paths["interactions"])
        self.data["topics"] = pd.read_csv(paths["topics"])

        self.log_action("Loaded CSV files")
        return "Data loaded successfully."

    def restore_backup(self):
        if not os.path.exists("backup.json"):
            raise FileNotFoundError("No backup.json file found. Save backup first.")

        with open("backup.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)

        self.data = {name: pd.DataFrame(records) for name, records in json_data.items()}
        self.log_action("Restored data from backup.json")
        return "Backup restored successfully."

    def clean_data(self):
        self._require_data("users", "posts", "interactions", "topics")

        users = self.data["users"].copy()
        posts = self.data["posts"].copy()
        interactions = self.data["interactions"].copy()
        topics = self.data["topics"].copy()

        if "text_preview" in posts.columns:
            posts.rename(columns={"text_preview": "content_preview"}, inplace=True)

        users.drop_duplicates(inplace=True)
        posts.drop_duplicates(inplace=True)
        interactions.drop_duplicates(inplace=True)
        topics.drop_duplicates(inplace=True)

        if "verified" in users.columns:
            users["verified"] = users["verified"].fillna(False)

        if "account_type" in users.columns:
            users["account_type"] = users["account_type"].fillna("personal")

        if "content_preview" in posts.columns:
            posts["content_preview"] = posts["content_preview"].fillna("No preview available")

        if "has_media" in posts.columns:
            posts["has_media"] = posts["has_media"].fillna(False)

        if "content_type" in posts.columns:
            posts["content_type"] = posts["content_type"].fillna("unknown")

        if "topic_id" in posts.columns and posts["topic_id"].isna().any():
            if posts["topic_id"].dropna().empty:
                posts = posts.dropna(subset=["topic_id"])
            else:
                posts["topic_id"] = posts["topic_id"].fillna(posts["topic_id"].mode()[0])

        if "interaction_type" in interactions.columns and interactions["interaction_type"].isna().any():
            if interactions["interaction_type"].dropna().empty:
                interactions = interactions.dropna(subset=["interaction_type"])
            else:
                interactions["interaction_type"] = interactions["interaction_type"].fillna(
                    interactions["interaction_type"].mode()[0]
                )

        if "moderation_level" in topics.columns and topics["moderation_level"].isna().any():
            if topics["moderation_level"].dropna().empty:
                topics = topics.dropna(subset=["moderation_level"])
            else:
                topics["moderation_level"] = topics["moderation_level"].fillna(
                    topics["moderation_level"].mode()[0]
                )

        if "description" in topics.columns:
            topics["description"] = topics["description"].fillna("No description provided")

        if "user_id" in users.columns:
            users.dropna(subset=["user_id"], inplace=True)

        if "post_id" in posts.columns:
            posts.dropna(subset=["post_id"], inplace=True)

        if "user_id" in posts.columns:
            posts.dropna(subset=["user_id"], inplace=True)

        if "topic_id" in posts.columns:
            posts.dropna(subset=["topic_id"], inplace=True)

        if "post_id" in interactions.columns:
            interactions.dropna(subset=["post_id"], inplace=True)

        if "topic_id" in topics.columns:
            topics.dropna(subset=["topic_id"], inplace=True)

        if "account_type" in users.columns:
            users = users[users["account_type"] != "bot"]

        if "user_id" in posts.columns and "user_id" in users.columns:
            posts = posts[posts["user_id"].isin(users["user_id"])]

        if "post_id" in interactions.columns and "post_id" in posts.columns:
            interactions = interactions[interactions["post_id"].isin(posts["post_id"])]

        self.data["users"] = users
        self.data["posts"] = posts
        self.data["interactions"] = interactions
        self.data["topics"] = topics

        self.log_action("Data cleaned, missing values filled, bots excluded")
        return "Data cleaned successfully."

    def save_backup(self):
        self._require_data("users", "posts", "interactions", "topics")

        json_data = {name: df.to_dict(orient="records") for name, df in self.data.items()}
        with open("backup.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)

        conn = sqlite3.connect("backup.db")
        for name, df in self.data.items():
            df.to_sql(name, conn, if_exists="replace", index=False)
        conn.close()

        self.log_action("Backup saved as JSON and SQLite")
        return "Backup saved as backup.json and backup.db."

    def merge_analysis(self):
        self._require_data("posts", "topics", "interactions")

        posts = self.data["posts"]
        topics = self.data["topics"]
        interactions = self.data["interactions"]

        merged = posts.merge(topics, on="topic_id", how="inner")
        merged = merged.merge(interactions, on="post_id", how="inner")

        reports = merged[merged["interaction_type"] == "report"]
        result = reports.groupby(["category", "moderation_level"]).size().reset_index(name="report_count")

        fig = Figure(figsize=(7.5, 4.5), dpi=100)
        ax = fig.add_subplot(111)
        if result.empty:
            ax.text(0.5, 0.5, "No report interactions found", ha="center", va="center")
            ax.set_axis_off()
        else:
            result.pivot(index="category", columns="moderation_level", values="report_count").fillna(0).plot(
                kind="bar", ax=ax
            )
            ax.set_title("Reports by Category and Moderation Level")
            ax.set_xlabel("Category")
            ax.set_ylabel("Report Count")
            ax.tick_params(axis="x", rotation=45)
            ax.legend(title="Moderation Level")
            fig.tight_layout()

        self.log_action("Report pattern analysis")
        return result, fig

    def pivot_analysis(self):
        self._require_data("posts", "topics")

        posts = self.data["posts"].copy()
        topics = self.data["topics"][["topic_id", "category"]].copy()

        posts["timestamp"] = pd.to_datetime(posts["timestamp"], errors="coerce")
        posts.dropna(subset=["timestamp"], inplace=True)
        posts["hour"] = posts["timestamp"].dt.hour

        merged = posts.merge(topics, on="topic_id", how="left")

        pivot = pd.pivot_table(
            merged,
            values="post_id",
            index="hour",
            columns="category",
            aggfunc="count",
            fill_value=0
        )

        fig = Figure(figsize=(7.5, 4.5), dpi=100)
        ax = fig.add_subplot(111)
        if pivot.empty:
            ax.text(0.5, 0.5, "No timestamped posts found", ha="center", va="center")
            ax.set_axis_off()
        else:
            heatmap = ax.imshow(pivot.values, aspect="auto")
            ax.set_title("Posting Activity by Hour and Topic")
            ax.set_ylabel("Hour of Day")
            ax.set_xlabel("Category")
            ax.set_xticks(range(len(pivot.columns)))
            ax.set_xticklabels(pivot.columns, rotation=45, ha="right")
            ax.set_yticks(range(len(pivot.index)))
            ax.set_yticklabels(pivot.index)
            fig.colorbar(heatmap, ax=ax, label="Post Count")
            fig.tight_layout()

        self.log_action("Generated pivot analysis")
        return pivot, fig

    def categorical_analysis(self):
        self._require_data("posts", "users", "topics")

        posts = self.data["posts"]
        users = self.data["users"]
        topics = self.data["topics"]

        merged = posts.merge(users, on="user_id", how="inner")
        merged = merged.merge(topics, on="topic_id", how="inner")

        table = pd.crosstab(
            [merged["verified"], merged["content_type"]],
            merged["moderation_level"]
        )

        self.log_action("Categorical analysis using verified, content_type, and moderation_level")
        return table

    def get_available_metrics(self):
        return ["likes_per_post", "comments_per_post", "shares_per_post", "reports_per_post", "total_engagements_per_post"]

    def _build_engagement_metrics(self):
        self._require_data("posts", "interactions")

        posts = self.data["posts"][["post_id"]].drop_duplicates().copy()
        interactions = self.data["interactions"].copy()

        counts = interactions.pivot_table(
            index="post_id",
            columns="interaction_type",
            values="interaction_id",
            aggfunc="count",
            fill_value=0
        )

        counts = counts.rename(columns={
            "like": "likes_per_post",
            "comment": "comments_per_post",
            "share": "shares_per_post",
            "report": "reports_per_post"
        })

        for col in ["likes_per_post", "comments_per_post", "shares_per_post", "reports_per_post"]:
            if col not in counts.columns:
                counts[col] = 0

        metrics = posts.merge(counts.reset_index(), on="post_id", how="left").fillna(0)
        metrics["total_engagements_per_post"] = (
            metrics["likes_per_post"] +
            metrics["comments_per_post"] +
            metrics["shares_per_post"] +
            metrics["reports_per_post"]
        )
        return metrics

    def calculate_stats(self, metric):
        metrics = self._build_engagement_metrics()

        if metric not in metrics.columns:
            raise ValueError(f"'{metric}' is not an available engagement metric.")

        series = pd.to_numeric(metrics[metric], errors="coerce").dropna()

        if series.empty:
            raise ValueError(f"Metric '{metric}' has no valid values.")

        mode_vals = series.mode()

        result = {
            "mean": series.mean(),
            "median": series.median(),
            "mode": mode_vals.iloc[0] if not mode_vals.empty else None
        }

        self.log_action(f"Calculated statistics for {metric}")
        return result

    def correlation_analysis(self):
        self._require_data("posts", "topics", "interactions")

        posts = self.data["posts"]
        topics = self.data["topics"]
        interactions = self.data["interactions"]

        merged = posts.merge(topics, on="topic_id", how="inner")
        merged = merged.merge(interactions, on="post_id", how="inner")

        merged["is_report"] = (merged["interaction_type"] == "report").astype(int)

        grouped = merged.groupby(["topic_id", "moderation_level"]).agg(
            total_interactions=("interaction_type", "count"),
            report_count=("is_report", "sum")
        ).reset_index()

        grouped["report_rate"] = grouped["report_count"] / grouped["total_interactions"]

        grouped["moderation_level_num"] = grouped["moderation_level"].astype(str).str.lower().map({
            "low": 1,
            "medium": 2,
            "high": 3
        })

        corr_data = grouped[["moderation_level_num", "report_count", "report_rate"]].dropna()

        if corr_data.empty:
            raise ValueError("No valid moderation data available for correlation analysis.")

        corr = corr_data.corr(numeric_only=True)

        fig = Figure(figsize=(6.5, 4.5), dpi=100)
        ax = fig.add_subplot(111)
        heatmap = ax.imshow(corr.values, aspect="auto", vmin=-1, vmax=1)
        ax.set_title("Moderation Level vs Report Count/Rate")
        ax.set_xticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=35, ha="right")
        ax.set_yticks(range(len(corr.index)))
        ax.set_yticklabels(corr.index)

        for row in range(len(corr.index)):
            for col in range(len(corr.columns)):
                ax.text(col, row, f"{corr.iloc[row, col]:.2f}", ha="center", va="center")

        fig.colorbar(heatmap, ax=ax, label="Correlation")
        fig.tight_layout()

        self.log_action("Generated correlation visualisation")
        return corr, fig

    def get_audit_log(self):
        try:
            with open("audit_log.txt", "r", encoding="utf-8") as f:
                content = f.read().strip()
            return content if content else "No audit log entries yet."
        except FileNotFoundError:
            return "No audit log entries yet."
